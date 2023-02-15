################################
# START OF: Initialization #####
################################

import pandas as pd
import numpy as np

from tqdm.auto import tqdm

import torch

from transformers import AutoTokenizer

import pytorch_lightning as pl

import pickle
import sys

from data_modules.BertDataModule import BertDataset
from models.BertFineTunerPl import BertFineTunerPl

RANDOM_SEED = 42

pl.seed_everything(RANDOM_SEED)

##############################
# END OF: Initialization #####
##############################


help_string = '\nUsage:  predict.py [OPTIONS]' \
              '\n' \
              '\nRequest prediction of the BERT model for all test arguments' \
              '\n' \
              '\nOptions:' \
              '\n  -h, --help               Display help text' \
              '\n  -i, --inputDataset       Directory with \'arguments.tsv\' file' \
              '\n  -o, --outputDir          Directory for writing the \'predictions.tsv\' file to'


def main(argv):
    dataset_dir = None
    model_dir = '/app/checkpoints/'
    output_dir = None

    try:
        opts, args = getopt.gnu_getopt(argv, "hi:o:", ["help", "inputDataset=", "outputDir="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_string)
            sys.exit()
        elif opt in ('-i', '--inputDataset'):
            dataset_dir = arg
        elif opt in ('-o', '--outputDir'):
            output_dir = arg

    ###############################
    # START OF: FUNCTIONALITY #####
    ###############################

    # CHANGED: './checkpoints/ to f'{model_dir}
    # CHANGED: "./data/ to f"{dataset_dir}
    PARAMS_ENSEMBLE = {
        "MODEL_CHECKPOINTS": [
            f'{model_dir}HCV-409-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-408-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-406-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-402-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-403-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-405-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-364-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-366-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-368-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-371-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-372-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt',
            f'{model_dir}HCV-375-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'
            ],
        "DESCRIPTION": "FULL #3xDebL_F1 3EP 3xdanRobL_F1 3EP 3xDebL_Loss 3EP 3xdanRobL_Loss 3EP",
        "TEST_PATH": f"{dataset_dir}arguments.tsv",
        "MAX_THRESHOLD_METRIC": "custom",
        "ENSEMBLE": "EN",
        "ENSEMBLE_THRESHOLD": 0.26,
        "LABEL_COLUMNS": ['Self-direction: thought',
                          'Self-direction: action',
                          'Stimulation',
                          'Hedonism',
                          'Achievement',
                          'Power: dominance',
                          'Power: resources',
                          'Face',
                          'Security: personal',
                          'Security: societal',
                          'Tradition',
                          'Conformity: rules',
                          'Conformity: interpersonal',
                          'Humility',
                          'Benevolence: caring',
                          'Benevolence: dependability',
                          'Universalism: concern',
                          'Universalism: nature',
                          'Universalism: tolerance',
                          'Universalism: objectivity']
    }

    # BLOCK #####

    NAME = ""
    ids = []
    for elem in PARAMS_ENSEMBLE["MODEL_CHECKPOINTS"]:
        # CHANGED: "checkpoints/" to model_dir
        text_list = elem.split(model_dir)[1]
        text_list = text_list.split("-")
        id = text_list[0] + "-" + text_list[1]
        ids.append(id)
        NAME = NAME + "_" + id
        print(text_list[0] + "-" + text_list[1])
    NAME = PARAMS_ENSEMBLE["ENSEMBLE"] + "_" + NAME[1:]

    PARAMS_ENSEMBLE["IDS"] = ids
    LABEL_COLUMNS = PARAMS_ENSEMBLE["LABEL_COLUMNS"]

    # BLOCK #####

    # Loading the parameters for each model
    PARAMS_LIST = []
    for id in PARAMS_ENSEMBLE["IDS"]:
        # CHANGED: ./checkpoints/ to {model_dir}
        with open(f'{model_dir}{id}_PARAMS.pkl', 'rb') as f:
            loaded_dict = pickle.load(f)
            PARAMS_LIST.append(loaded_dict)

    # BLOCK #####

    # Concatenating relevant information into one Ensemble_list
    ENSEMBLE_LIST = []
    for param, id, mc in zip(PARAMS_LIST, PARAMS_ENSEMBLE["IDS"], PARAMS_ENSEMBLE["MODEL_CHECKPOINTS"]):
        ENSEMBLE_LIST.append({"PARAMS": param, "ID": id, "MODEL_CHECKPOINT": mc})

    # BLOCK #####

    test_df_input = pd.read_csv(PARAMS_ENSEMBLE["TEST_PATH"], sep='\t')

    # BLOCK #####

    test_df_input["text"] = test_df_input["Premise"] + " " + test_df_input["Stance"] + " " + test_df_input["Conclusion"]

    # BLOCK #####

    def predict_unseen_data(trained_model, data):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        trained_model = trained_model.to(device)

        silver_df_dataset = BertDataset(
            data=data,
            tokenizer=TOKENIZER,
            max_token_count=PARAMS["MAX_TOKEN_COUNT"],
        )

        predictions = []

        for item in tqdm(silver_df_dataset):
            _, prediction = trained_model(
                item["input_ids"].unsqueeze(dim=0).to(device),
                item["attention_mask"].unsqueeze(dim=0).to(device)
            )
            predictions.append(prediction.flatten())

        predictions = torch.stack(predictions).detach().cpu()

        return predictions

    # BLOCK #####

    predictions = []
    for idx, elem in enumerate(ENSEMBLE_LIST):
        print(f"Starting with model {elem['MODEL_CHECKPOINT']}")
        PARAMS = elem["PARAMS"]
        trained_model = BertFineTunerPl.load_from_checkpoint(
            elem["MODEL_CHECKPOINT"],
            params=PARAMS,
            label_columns=LABEL_COLUMNS,
            n_classes=len(LABEL_COLUMNS)
        )
        trained_model.eval()
        trained_model.freeze()
        print(f"With Tokenizer {PARAMS['MODEL_PATH']}")
        TOKENIZER = AutoTokenizer.from_pretrained(PARAMS["MODEL_PATH"])
        pred = predict_unseen_data(trained_model=trained_model, data=test_df_input)
        predictions.append(pred)

    # BLOCK #####

    predictions = torch.stack(predictions).numpy()
    predictions_avg = np.mean(predictions, axis=0)

    # BLOCK #####

    upper, lower = 1, 0

    # Use optimal decision threshold.
    y_pred = np.where(predictions_avg > PARAMS_ENSEMBLE["ENSEMBLE_THRESHOLD"], upper, lower)

    # BLOCK #####

    prediction_dictionary = {}
    prediction_dictionary["Argument ID"] = test_df_input["Argument ID"]
    for idx, l_name in enumerate(LABEL_COLUMNS):
        prediction_dictionary[l_name] = y_pred[:, idx]

    test_prediction_df = pd.DataFrame(prediction_dictionary)
    test_prediction_df.head()

    # BLOCK #####

    # CHANGED: ./submission_test to {output_dir}predictions
    test_prediction_df.to_csv(f"{output_dir}predictions.tsv", sep="\t", index=False)

    #############################
    # END OF: FUNCTIONALITY #####
    #############################


if __name__ == '__main__':
    main(sys.argv[1:])
