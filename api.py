from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints
from typing import Annotated

from ml_classifier import MLTaskClassifier


app = FastAPI(title="Mini AI Task Classifier API")
clf = MLTaskClassifier()


class TaskRequest(BaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=10000)]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: TaskRequest):
    category = clf.predict(req.text)
    return {"text": req.text, "category": category}