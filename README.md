# Mini AI Task Classifier

Educational text-classification API using FastAPI, CountVectorizer and MultinomialNB.
The dataset has **10 examples across five categories**. Accuracy has not been measured
on a held-out dataset; this is a learning prototype, not a production classifier.

## Run (Python 3.10+)

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload
```

Open http://127.0.0.1:8000/docs. `GET /health` checks the service.
`POST /predict` accepts `{"text":"refund request"}` and returns
`{"text":"refund request","category":"Support"}`. Blank input returns HTTP 422.
For the terminal interface, run `python main.py`.

On first startup the model is trained from the bundled `data.json` and saved to
`model.pkl` beside the source. Subsequent starts load that file. Delete the generated
file to retrain after editing the dataset. Only load model files you trust: joblib
serialization is not safe for untrusted files. No login or rate limiting is provided.

## Tests

```sh
pip install -r requirements-dev.txt
python -m pytest -q
```
