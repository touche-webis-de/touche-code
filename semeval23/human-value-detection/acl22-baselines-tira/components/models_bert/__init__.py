"""
    Collection of machine learning functions regarding the models:
    Bert

    Functions
    ---------
    train_bert_model(train_dataframe, model_dir, labels, test_dataframe=None, num_train_epochs=20):
        Train Bert model
    predict_bert_model(dataframe, model_dir, labels):
        Predict with Bert model
    """
from .bert import (train_bert_model, predict_bert_model, load_tokenizer, pre_load_saved_model)
