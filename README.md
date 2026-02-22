# 🚀 Mini AI Task Classifier (FastAPI + scikit-learn)

A lightweight Machine Learning API that classifies short business-related tasks into predefined categories such as Support, Finance, or Sales.

This project demonstrates how to combine a trained scikit-learn model with a FastAPI backend for real-time predictions.

---

## 🎯 What This Project Does

The API receives a short text input and returns a predicted task category.

Example:

Input:
"Please refund the customer for the last order"

Output:
"Support"

---

## ✨ Features

- Text classification using scikit-learn
- Pre-trained model stored as `model.pkl`
- Dataset stored in `data.json`
- FastAPI REST endpoint for predictions
- Clean modular structure (separated ML logic & API logic)
- Easy to extend with more data or categories

---

## 🧰 Tech Stack

- Python 3.x
- FastAPI
- Uvicorn
- scikit-learn
- pickle (model persistence)

---

## 🗂 Project Structure

mini-ai-task-classifier/

api.py                → API routes  
main.py               → FastAPI app entry point  
classifier.py         → Classification wrapper  
ml_classifier.py      → ML training & model logic  
data.json             → Training dataset  
model.pkl             → Trained model  
requirements.txt  
README.md  

---

## ⚙️ Setup (Run Locally)

### 1️⃣ Create Virtual Environment

python3 -m venv venv  
source venv/bin/activate  

### 2️⃣ Install Dependencies

pip install -r requirements.txt  

### 3️⃣ Run the API

uvicorn main:app --reload  

Server:
http://127.0.0.1:8000  

Swagger UI:
http://127.0.0.1:8000/docs  

---

## 🔌 API Endpoint

### POST /predict

Request Body:

{
  "text": "Call the client and discuss pricing"
}

Response:

{
  "prediction": "Sales"
}

---

## 🧠 How It Works

1. Text input is vectorized using a text feature extraction method.
2. The trained scikit-learn model predicts the category.
3. The prediction is returned via FastAPI.

The model is pre-trained and loaded from `model.pkl`.

---

## 🎯 Why This Project (For Werkstudent Applications)

This project demonstrates:

- Practical ML integration inside a backend API
- Separation of concerns (ML logic vs API logic)
- Model persistence and loading
- Real-world API design
- Clean modular Python structure

---

## 👤 Author

Hesam Shahbazi