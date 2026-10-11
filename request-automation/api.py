import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from workflow import Workflow, Conflict


def create_app(path=None):
    workflow = Workflow(path or os.getenv('WORKFLOW_DB', 'data/requests.db'))
    app = FastAPI(title='Request Automation — local learning demo')

    class Request(BaseModel):
        key: str = Field(min_length=1, max_length=128)
        text: str = Field(min_length=1, max_length=10000)

    @app.post('/requests', status_code=201)
    def submit(request: Request):
        try:
            return {'id': workflow.submit(request.key, request.text)}
        except Conflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get('/requests/{job_id}')
    def get(job_id: int):
        result = workflow.get(job_id)
        if result is None:
            raise HTTPException(404, 'Request not found')
        return result

    return app
