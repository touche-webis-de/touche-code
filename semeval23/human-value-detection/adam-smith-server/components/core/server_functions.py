import logging
import numpy as np
import pandas as pd
import torch
from components.data_modules.BertDataModule import BertDataset
from components.interface_modules.load_ensemble_list import (load_ensemble_list)
from components.interface_modules.transformer_local import (load_local_tokenizer)
from components.models.BertFineTunerPl import BertFineTunerPl

__model_dir__ = '/app/checkpoints/human_value_trained_models'

__model_registry__ = {}

__ensemble_threshold__ = 0.26

__ensemble_list__ = []

__label_columns__ = []


def setup(threshold: float):
    global __model_registry__
    global __ensemble_threshold__
    global __ensemble_list__
    global __label_columns__

    __ensemble_threshold__ = threshold
    _, ENSEMBLE_LIST, LABEL_COLUMNS, NAME = load_ensemble_list(__model_dir__, threshold)
    __label_columns__ = LABEL_COLUMNS
    __ensemble_list__ = ENSEMBLE_LIST

    logging.info(f'Initializing with configuration: {NAME}')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    for idx, elem in enumerate(ENSEMBLE_LIST):
        logging.debug(f"Loading model {elem['MODEL_CHECKPOINT']}")

        PARAMS = elem["PARAMS"]
        TRAINED_MODEL = BertFineTunerPl.load_from_checkpoint(
            elem["MODEL_CHECKPOINT"],
            params=PARAMS,
            label_columns=LABEL_COLUMNS,
            n_classes=len(LABEL_COLUMNS)
        )
        TRAINED_MODEL.eval()
        TRAINED_MODEL.freeze()
        TRAINED_MODEL = TRAINED_MODEL.to(device)
        __model_registry__[elem['MODEL_CHECKPOINT']] = TRAINED_MODEL

        logging.debug(f"With Tokenizer {PARAMS['MODEL_PATH']}")
        if PARAMS['MODEL_PATH'] not in __model_registry__.keys():
            TOKENIZER = load_local_tokenizer(PARAMS["MODEL_PATH"])
            __model_registry__[PARAMS['MODEL_PATH']] = TOKENIZER


def predict_argument(argument: str):
    data = pd.DataFrame([argument], columns=['text'])

    predictions = []
    for idx, elem in enumerate(__ensemble_list__):
        logging.debug(f'Classifying with {elem["MODEL_CHECKPOINT"]}')
        TRAINED_MODEL = __model_registry__[elem["MODEL_CHECKPOINT"]]
        PARAMS = elem["PARAMS"]
        TOKENIZER = __model_registry__[PARAMS['MODEL_PATH']]
        try:
            pred = __predict_unseen_data__(
                trained_model=TRAINED_MODEL,
                model_tokenizer=TOKENIZER,
                params=PARAMS,
                data=data
            )
            predictions.append(pred)
        except BaseException as e:
            logging.error(f'Exception while running model \'{elem["MODEL_CHECKPOINT"]}\': {str(e)}')
            return None

    predictions = torch.stack(predictions).numpy()
    predictions_avg = np.mean(predictions, axis=0)

    upper, lower = 1, 0
    y_pred = np.where(predictions_avg > __ensemble_threshold__, upper, lower)

    prediction_dictionary = {}
    for idx, l_name in enumerate(__label_columns__):
        prediction_dictionary[l_name] = str(y_pred[0, idx])

    return prediction_dictionary


def __predict_unseen_data__(trained_model, model_tokenizer, params, data):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    silver_df_dataset = BertDataset(
        data=data,
        tokenizer=model_tokenizer,
        max_token_count=params["MAX_TOKEN_COUNT"],
    )

    predictions = []

    for item in silver_df_dataset:
        _, prediction = trained_model(
            item["input_ids"].unsqueeze(dim=0).to(device),
            item["attention_mask"].unsqueeze(dim=0).to(device)
        )
        predictions.append(prediction.flatten())

    predictions = torch.stack(predictions).detach().cpu()

    return predictions
