import getopt
import os
import sys

from models.interface_modules.transformer_local import (load_local_tokenizer)
from models.interface_modules.load_ensemble_list import (load_ensemble_list)

################################
# START OF: Initialization #####
################################

import pandas as pd
import numpy as np

from tqdm.auto import tqdm

import torch

# CHANGED: Removed unused import of AutoTokenizer

import pytorch_lightning as pl

# CHANGED: Removed unused import of pickle

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
    model_dir = '/app/checkpoints/human_value_trained_models'
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

    if not os.path.isdir(model_dir):
        print('No models detected')
        sys.exit(2)

    ###############################
    # START OF: FUNCTIONALITY #####
    ###############################

    # CHANGED: outsourced generation of ensemble data to models/interface_modules/load_ensemble_list.py
    PARAMS_ENSEMBLE, ENSEMBLE_LIST, LABEL_COLUMNS, NAME = load_ensemble_list(model_dir, dataset_dir)

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
        # Changed to load pre-downloaded tokenizer
        # TOKENIZER = AutoTokenizer.from_pretrained(PARAMS["MODEL_PATH"])
        TOKENIZER = load_local_tokenizer(PARAMS["MODEL_PATH"])
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

    # CHANGED: Added lines
    prediction_file = os.path.join(output_dir, "predictions.tsv")
    print(f'Writing prediction to: {prediction_file}')
    # CHANGED: "./submission_test/..." prediction_file
    test_prediction_df.to_csv(prediction_file, sep="\t", index=False)

    #############################
    # END OF: FUNCTIONALITY #####
    #############################


if __name__ == '__main__':
    main(sys.argv[1:])
