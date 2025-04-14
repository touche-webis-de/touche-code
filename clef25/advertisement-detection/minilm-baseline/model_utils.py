from abc import ABC
from datasets import Dataset
import pandas as pd
from pathlib import Path
import spacy
import torch as T
from torch.utils.data import DataLoader
from transformers import AutoModel, AutoTokenizer
from typing import Any, Dict, List

from models import SupervisedModel

MODEL_PATH = Path(__file__).parent / "models"
DEVICE = T.device("cuda" if T.cuda.is_available() else "cpu")


class ModelWrapper(ABC):
    def __init__(self, model_name: str, input_run: List[Dict[str, Any]], device: T.device = None):
        self.model_name = model_name
        self.input_run = input_run
        self.device = device or DEVICE
        self.tokenizer = None

        self.weight_path = MODEL_PATH / f"{model_name}.pt"

        self.tokenized_ds = None
        self.response_df = pd.DataFrame()
        self.prediction_df = pd.DataFrame()


class SBertModel(ModelWrapper):
    def __init__(self, model_name: str, input_run: List[Dict[str, Any]], device: T.device = None):
        super().__init__(model_name, input_run=input_run, device=device)
        self.tokenizer = AutoTokenizer.from_pretrained(f"sentence-transformers/{model_name}")
        self.model = SupervisedModel(sbert_model=model_name)

    def prepare_dataset(self):
        # 1. Store the DataFrame of responses
        self.response_df = self.input_run

        # 2. Split the responses into sentence pairs
        nlp = spacy.load("en_core_web_sm")
        tmp = [_split_into_sentence_pairs(response=res, id=id, topic=topic, nlp=nlp) 
               for res, id, topic in zip(self.input_run["response"], self.input_run["id"], self.input_run["meta_topic"])]
        list_of_dicts = [d for x in tmp for d in x["sentence_pairs"]]
        dataset = (Dataset.from_dict({'pairs': list_of_dicts}).flatten()
                   .rename_column("pairs.sentence1", "sentence1")
                   .rename_column('pairs.sentence2', "sentence2")
                   .rename_column('pairs.response_id', "response_id")
                   .rename_column('pairs.topic', "topic")
                   .rename_column('pairs.pair_num', "pair_num")
                   )

        # 3. Tokenize the dataset
        remove_columns = ["sentence1", "sentence2"]
        tokenized_ds = dataset.map(lambda example: self._tokenize_function(example),
                                   remove_columns=remove_columns)
        self.tokenized_ds = tokenized_ds.with_format("torch")

    def _tokenize_function(self, example):
        # Return the tokenized strings (Note: They are in one array)
        # Pad to the maximum length of the model
        return self.tokenizer(example["sentence1"], example["sentence2"], padding="max_length", truncation=True)

    def make_predictions(self, batch_size: int = 16):
        if self.tokenized_ds is None:
            self.prepare_dataset()

        # Prepare model and dataloader
        encoder_weights = T.load(self.weight_path, weights_only=True, map_location=self.device)
        model = self.model.to(self.device)
        model.load_state_dict(encoder_weights)

        test_dl = DataLoader(self.tokenized_ds.with_format("torch", device=self.device), batch_size=batch_size)

        # Perform evaluation
        model.eval()
        with T.no_grad():
            # Initialize lists to store batch values
            ids, topics, predictions, pair_nums = ([] for i in range(4))

            for batch in test_dl:
                # Get batch values
                ids += batch.pop('response_id')
                topics += batch.pop('topic')
                pair_nums += [int(num.item()) for num in batch.pop('pair_num')]

                # Get the logits from the batch
                predictions += [int(logit.item() > 0.5) for logit in model(batch=batch)]

        self.prediction_df = pd.DataFrame({"response_id": ids,
                                           "topic": topics,
                                           "pair_num": pair_nums,
                                           "prediction": predictions})

        # Check if at least one sentence pair was predicted positively and join the result into self.response_df
        tmp = self.prediction_df.groupby("response_id")["prediction"].max().reset_index()
        self.response_df = self.response_df[["id"]]
        self.response_df = pd.merge(self.response_df, tmp, left_on="id", right_on="response_id")

        # Create and return predictions
        return self.response_df[["id", "prediction"]]


def _split_into_sentence_pairs(response, id, topic, nlp):
    result = {'sentence_pairs': []}
    sentences = [str(s).strip() for s in nlp(response.strip()).sents]
    result['sentence_pairs'] = [{"response_id": id,
                                 "topic": topic,
                                 "sentence1": sentences[i],
                                 "sentence2": sentences[i + 1],
                                 "pair_num": i
                                 }
                                for i in range(len(sentences[:-1]))]
    return result
