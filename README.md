Mini AI Task Classifier

A simple machine learning project that classifies business tasks into categories such as Support, Finance, Sales, and Management.

Features

	•Text classification using machine learning
	•Built with scikit-learn
	•REST API using FastAPI
	•Model trained on custom dataset
	•Interactive CLI version
	•API version for external integration

Tech Stack

	•Python
	•scikit-learn
	•FastAPI
	•Uvicorn
	•Git

Project Structure

	mini-ai-task-classifier/
	│
	├── api.py               # FastAPI application
	├── main.py              # CLI version
	├── ml_classifier.py     # Machine learning logic
	├── classifier.py        # Legacy/simple classifier
	├── data.json            # Training dataset
	├── model.pkl            # Trained model file
	├── requirements.txt     # Python dependencies
	├── README.md            # Project documentation
	└── .gitignore           # Ignored files

How it works

The model converts input text into numerical features using CountVectorizer and trains a Multinomial Naive Bayes classifier on labeled examples.

Users can:

	•Run it in terminal
	•Send HTTP requests to the API endpoint /predict
