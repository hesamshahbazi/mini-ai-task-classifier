import json
import os
from pathlib import Path
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class MLTaskClassifier:
    def __init__(self, model_path=None) -> None:
        self.base_dir = Path(__file__).resolve().parent
        self.model_path = Path(model_path) if model_path is not None else self.base_dir / "model.pkl"
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()

        
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            
            texts, labels = self._load_data()
            X = self.vectorizer.fit_transform(texts)
            self.model.fit(X, labels)
            self.save_model()

    def save_model(self) -> None:
        joblib.dump((self.vectorizer, self.model), self.model_path)

    def load_model(self) -> None:
        self.vectorizer, self.model = joblib.load(self.model_path)

    def _load_data(self):
        with open(self.base_dir / "data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        texts = [item["text"] for item in data["training"]]
        labels = [item["label"] for item in data["training"]]
        return texts, labels

    def predict(self, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must not be blank")
        X = self.vectorizer.transform([text.strip()])
        return self.model.predict(X)[0]