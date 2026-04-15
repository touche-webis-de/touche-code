from abc import ABC
from datasets import Dataset
from itertools import groupby
from operator import itemgetter
import pandas as pd
from pathlib import Path
import spacy
import torch as T
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from typing import Any, Dict, List

from models import SentenceClassifier

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
        self.model = SentenceClassifier(sbert_model=model_name)

    def prepare_dataset(self):
        # 1. Store the DataFrame of responses
        self.response_df = self.input_run

        # 2. Split the responses into sentence pairs and add the spans to the response_df
        nlp = spacy.load("en_core_web_sm")
        tmp = [_split_into_sentence_pairs(response=res, id=id, nlp=nlp)
               for res, id in zip(self.input_run["response"], self.input_run["id"])]

        self.response_df["sentence_spans"] = [x["sentence_spans"] for x in tmp]

        list_of_dicts = [d for x in tmp for d in x["sentence_pairs"]]
        dataset = (Dataset.from_dict({'pairs': list_of_dicts}).flatten()
                   .rename_column("pairs.sentence1", "sentence1")
                   .rename_column('pairs.sentence2', "sentence2")
                   .rename_column('pairs.response_id', "response_id")
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
            ids, predictions, pair_nums = ([] for i in range(3))

            for batch in test_dl:
                # Get batch values
                ids += batch.pop('response_id')
                pair_nums += [int(num.item()) for num in batch.pop('pair_num')]

                # Get the logits from the batch
                predictions += [int(logit.item() > 0.5) for logit in model(batch=batch)]

        df = pd.DataFrame({"response_id": ids,
                           "pair_num": pair_nums,
                           "label": predictions})

        # Merge the predictions with the response_df to get the spans of the predictions
        df = (df
            .loc[df["label"] == 1]
            .groupby("response_id")
            .agg({"pair_num": list})
            .reset_index()
        )
        self.prediction_df = (
            pd.merge(self.response_df[["id", "sentence_spans"]], df,
                     left_on="id",
                     right_on="response_id",
                     how="left")
            .drop("response_id", axis=1)
        )
        self.prediction_df["spans"] = self.prediction_df.apply(
            lambda row: get_detected_spans(pair_nums=row["pair_num"], sentence_spans=row["sentence_spans"]), axis=1
        )

        # Return predictions
        return self.prediction_df[["id", "spans"]]


def _split_into_sentence_pairs(response, id, nlp):
    result = {'sentence_pairs': [], 'sentence_spans': []}
    sentences = []
    sentence_spans = []
    for sent in nlp(response.strip()).sents:
        sentences.append(sent.text.strip())
        sentence_spans.append((sent.start_char, sent.end_char))

    result['sentence_pairs'] = [{"response_id": id,
                                 "sentence1": sentences[i],
                                 "sentence2": sentences[i + 1],
                                 "pair_num": i
                                 }
                                for i in range(len(sentences[:-1]))]
    result['sentence_spans'] = sentence_spans
    return result


def get_detected_spans(pair_nums: list[int], sentence_spans: list[tuple[int, int]]):
    if not isinstance(pair_nums, list):
        return []

    # Form lists of consecutive pairs
    pair_num = sorted(pair_nums)
    consecutive_num = []
    for k, g in groupby(enumerate(pair_num), lambda x: x[0] - x[1]):
        consecutive_num.append(list(map(itemgetter(1), g)))

    # Loop over all lists of consecutive numbers to get spans
    ad_spans = []
    for num_list in consecutive_num:
        if len(num_list) >= 2:
            ad_spans += get_detection_multiple(num_list=num_list, sentence_spans=sentence_spans)
        else:
            ad_spans += get_detection_single(num=num_list[0], sentence_spans=sentence_spans)

    return ad_spans


def get_detection_multiple(num_list: list[int], sentence_spans: list[tuple[int, int]]):
    spans_with_ads = [(sentence_spans[i], sentence_spans[i+1]) for i in num_list]
    injection_pairs = len(spans_with_ads)

    predicted_spans = []
    for i, (span1, span2) in enumerate(spans_with_ads):
        if i + 1 == injection_pairs:
            predicted_spans.append(span1)
        else:
            predicted_spans.append(span2)

    return predicted_spans[:-1]


def get_detection_single(num: int, sentence_spans: list[tuple[int, int]]):
    # Handle predictions for the first and last pair -> Only the "outer sentence" contains ad
    if num == 0:
        return sentence_spans[0]
    if num + 1 == len(sentence_spans) - 1:
        return sentence_spans[-1]

    # For pairs in the middle, we can't say which sentence was chosen
    tup = (sentence_spans[num], sentence_spans[num+1])
    return [tup[0], tup[1]]