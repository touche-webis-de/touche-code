"""
    Collection of machine learning functions regarding the models:
    Support Vector Machine (SVM)

    Functions
    ---------
    train_svm(train_dataframe, labels, vectorizer_file, model_file, test_dataframe=None):
        Train Support Vector Machines (SVMs)
    predict_svm(dataframe, labels, vectorizer_file, model_file):
        Predict with Support Vector Machines (SVMs)
    """
from .svm import (train_svm, load_svms)
