import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from fastapi.testclient import TestClient
from api import create_app
from workflow import Workflow, Conflict

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'jobs.db'
        self.flow = Workflow(self.path)

    def test_idempotency_and_conflict(self):
        job = self.flow.submit('a', 'refund')
        self.assertEqual(job, self.flow.submit('a', 'refund'))
        with self.assertRaises(Conflict):
            self.flow.submit('a', 'other')

    def test_persistence_and_triage(self):
        job = self.flow.submit('a', 'urgent refund')
        Workflow(self.path).run_one()
        record = self.flow.get(job)
        self.assertEqual(record['status'], 'completed')
        self.assertEqual(record['result']['category'], 'billing')
        self.assertEqual(record['result']['priority'], 'high')
        self.assertEqual(len(record['events']), 3)

    def test_retry_backoff_and_terminal_failure(self):
        job = self.flow.submit('a', 'hello')
        def fail(text):
            raise RuntimeError('secret must not enter database')
        self.flow.run_one(fail, now=100)
        self.assertIsNone(self.flow.run_one(fail, now=101))
        self.flow.run_one(fail, now=102)
        self.flow.run_one(fail, now=106)
        self.assertEqual(self.flow.get(job)['status'], 'failed')
        self.assertEqual(self.flow.get(job)['error'], 'RuntimeError')
        self.assertIsNone(self.flow.run_one(fail, now=200))

    def test_retry_then_success(self):
        job = self.flow.submit('a', 'hello')
        self.flow.run_one(lambda _: 1/0, now=10)
        self.flow.run_one(now=12)
        self.assertEqual(self.flow.get(job)['status'], 'completed')
        self.assertIsNone(self.flow.get(job)['error'])

    def test_concurrent_submissions_and_workers(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            ids = list(pool.map(lambda _: self.flow.submit('same', 'login error'), range(8)))
        self.assertEqual(len(set(ids)), 1)
        with ThreadPoolExecutor(max_workers=4) as pool:
            processed = list(pool.map(lambda _: self.flow.run_one(), range(8)))
        self.assertEqual(sum(p is not None for p in processed), 1)

    def test_api_validation_conflict_and_missing(self):
        with TestClient(create_app(self.path)) as client:
            self.assertEqual(client.post('/requests', json={'key':'x', 'text':'  '}).status_code, 422)
            response = client.post('/requests', json={'key':'x','text':'invoice'})
            self.assertEqual(response.status_code, 201)
            self.assertEqual(client.get('/requests/1').status_code, 200)
            self.assertEqual(client.post('/requests', json={'key':'x','text':'different'}).status_code, 409)
            self.assertEqual(client.get('/requests/999').status_code, 404)
