"""Durable, rules-based request triage. No external messages are sent."""
import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path


class Conflict(ValueError):
    pass


class Workflow:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY, request_key TEXT UNIQUE NOT NULL,
                    payload TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
                    attempts INTEGER NOT NULL DEFAULT 0, available REAL NOT NULL DEFAULT 0,
                    result TEXT, error TEXT);
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY, job_id INTEGER NOT NULL,
                    status TEXT NOT NULL, created REAL NOT NULL);
            ''')

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def event(db, job_id, status, now):
        db.execute('INSERT INTO events(job_id,status,created) VALUES(?,?,?)', (job_id, status, now))

    def submit(self, key, text):
        if not isinstance(key, str) or not key.strip() or len(key) > 128:
            raise ValueError('key must contain 1–128 characters')
        if not isinstance(text, str) or not text.strip() or len(text) > 10000:
            raise ValueError('text must contain 1–10000 characters')
        key, text = key.strip(), text.strip()
        payload = json.dumps({'text': text}, sort_keys=True)
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            existing = db.execute('SELECT * FROM jobs WHERE request_key=?', (key,)).fetchone()
            if existing:
                if existing['payload'] != payload:
                    raise Conflict('key already used with different content')
                return existing['id']
            job_id = db.execute('INSERT INTO jobs(request_key,payload) VALUES(?,?)', (key, payload)).lastrowid
            self.event(db, job_id, 'pending', time.time())
            return job_id

    def get(self, job_id):
        with self.db() as db:
            row = db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
            if row is None:
                return None
            result = dict(row)
            result['payload'] = json.loads(result['payload'])
            result['result'] = json.loads(result['result']) if result['result'] else None
            result['events'] = [dict(e) for e in db.execute('SELECT status,created FROM events WHERE job_id=? ORDER BY id', (job_id,))]
            return result

    def run_one(self, handler=None, now=None):
        """Atomic local processing; crash rolls back. Handler MUST have no side effects.

        Holding the write transaction intentionally serializes this small demo.
        Do not put network calls here; production workers need leases/outbox design.
        """
        handler = handler or triage
        now = time.time() if now is None else now
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT * FROM jobs WHERE status IN ('pending','retry') AND available<=? ORDER BY id LIMIT 1", (now,)).fetchone()
            if row is None:
                return None
            attempt = row['attempts'] + 1
            self.event(db, row['id'], 'processing', now)
            try:
                result = json.dumps(handler(json.loads(row['payload'])['text']))
            except Exception as exc:
                status = 'failed' if attempt >= 3 else 'retry'
                db.execute('UPDATE jobs SET status=?,attempts=?,available=?,error=? WHERE id=?',
                           (status, attempt, now + 2 ** attempt, type(exc).__name__, row['id']))
            else:
                status = 'completed'
                db.execute("UPDATE jobs SET status='completed',attempts=?,result=?,error=NULL WHERE id=?", (attempt, result, row['id']))
            self.event(db, row['id'], status, now)
            return row['id']


def triage(text):
    lowered = text.casefold()
    category = 'billing' if any(w in lowered for w in ('invoice', 'refund', 'payment')) else 'technical' if any(w in lowered for w in ('error', 'crash', 'login')) else 'general'
    priority = 'high' if any(w in lowered for w in ('urgent', 'outage')) else 'normal'
    return {'category': category, 'priority': priority, 'review_required': True,
            'draft': f'Thank you. Your {category} request has been queued for human review.'}
