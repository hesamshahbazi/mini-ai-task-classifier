from fastapi import FastAPI
from pydantic import BaseModel

from ml_classifier import MLTaskClassifier


app = FastAPI(title="Mini AI Task Classifier API")
clf = MLTaskClassifier()


class TaskRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: TaskRequest):
    category = clf.predict(req.text)
    return {"text": req.text, "category": category}