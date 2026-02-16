import json
import os
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class MLTaskClassifier:
    def __init__(self) -> None:
        self.model_path = "model.pkl"
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
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        texts = [item["text"] for item in data["training"]]
        labels = [item["label"] for item in data["training"]]
        return texts, labels

    def predict(self, text: str) -> str:
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]