#!/usr/bin/env python3
from pathlib import Path

from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from tira.rest_api_client import Client

if __name__ == "__main__":

    # Load the data
    tira = Client()
    text = tira.pd.inputs("ads-in-rag-task-1-detection-training-20260422-training")
    text = text.set_index("id")

    labels = tira.pd.truths("ads-in-rag-task-1-detection-training-20260422-training")
    df = text.join(labels.set_index("id"))

    # Train the model
    model = Pipeline(
        [
            ("vectorizer", TfidfVectorizer()),
            ("classifier", MultinomialNB()),
        ]
    )

    model.fit(df["response"], df["label"])

    # Save the model
    dump(model, Path(__file__).parent / "model.joblib")