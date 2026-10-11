# Request Automation

AI-assisted learning project using Python, FastAPI and SQLite. Standalone: does not import the parent project's experimental ML classifier. Categorization uses English keyword rules, not a trained AI model.

## Run

Python 3.11+. Run these commands **inside request-automation/**:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python worker.py --demo --db data/demo.db
uvicorn api:create_app --factory --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs. POST `/requests` with:

```json
{"key":"support-001","text":"Urgent login error during an outage"}
```

In another terminal with the same working directory and environment:

```sh
python worker.py --watch
```

GET `/requests/1` displays status, result and audit events. API and worker default to `data/requests.db`. If setting API environment variable `WORKFLOW_DB`, pass the same path as worker `--db`. Without `--watch`, worker processes currently eligible jobs and exits; future retries require another invocation.

## Behavior

Intake → persistent pending job → category/priority → draft for human review. No messages are sent. Duplicate key and same text return the existing ID; different content returns 409. Whitespace-only requests are rejected.

A SQLite write transaction serializes local processing and commits result plus audit events together. A crash before commit rolls back. Exceptions retry after 2 then 4 seconds, with terminal failure after three attempts. Only exception type is recorded.

## Verify

```sh
python -m unittest discover -s tests -v
```

Six tests cover API validation, key conflicts, persistence, triage, backoff, terminal failure, recovery and concurrent submissions/workers. Tests use temporary databases and no paid API.

## Limits

Local learning demo: no authentication, rate limiting, encryption or retention automation. Keep the API on loopback and use synthetic data. English keyword rules can misclassify; drafts need human review.

Processing holds a database write lock: the handler must be short and side-effect-free. Never add network/email calls here. Production delivery needs an outbox, idempotent consumers and worker leases. This is not a high-throughput queue or production deployment.

## Before using on a CV

Study and explain transactions, idempotency, HTTP 409 and retries; change a rule and test it. Honest description: “AI-assisted learning project for request triage using Python, FastAPI and SQLite, with idempotent intake, bounded retries and automated tests.” No independent proficiency, production use or business impact is established merely by creating this project.
