import pickle
import os


def load_ensemble_list(model_dir: str, dataset_dir: str, verbose: bool = False):

    if not model_dir.endswith(os.path.sep):
        model_dir += os.path.sep
    if not dataset_dir.endswith(os.path.sep):
        dataset_dir += os.path.sep

    #####################################
    # START OF: ENSEMBLE data setup #####
    #####################################

    # CHANGED: './checkpoints/...' to os.path.join(model_dir, '...')
    # CHANGED: "./data/arguments-test.tsv" to os.path.join(dataset_dir, 'arguments.tsv')
    PARAMS_ENSEMBLE = {
        "MODEL_CHECKPOINTS": [
            os.path.join(model_dir, 'HCV-409-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-408-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-406-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-402-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-403-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-405-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-364-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-366-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-368-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-371-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-372-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt'),
            os.path.join(model_dir, 'HCV-375-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt')
        ],
        "DESCRIPTION": "FULL #3xDebL_F1 3EP 3xdanRobL_F1 3EP 3xDebL_Loss 3EP 3xdanRobL_Loss 3EP",
        "TEST_PATH": os.path.join(dataset_dir, 'arguments.tsv'),
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
        if verbose:
            print(text_list[0] + "-" + text_list[1])
    NAME = PARAMS_ENSEMBLE["ENSEMBLE"] + "_" + NAME[1:]

    PARAMS_ENSEMBLE["IDS"] = ids
    LABEL_COLUMNS = PARAMS_ENSEMBLE["LABEL_COLUMNS"]

    # BLOCK #####

    # Loading the parameters for each model
    PARAMS_LIST = []
    for id in PARAMS_ENSEMBLE["IDS"]:
        # CHANGED: f'./checkpoints/...' to os.path.join(model_dir, f'...')
        with open(os.path.join(model_dir, f'{id}_PARAMS.pkl'), 'rb') as f:
            loaded_dict = pickle.load(f)
            PARAMS_LIST.append(loaded_dict)

    # BLOCK #####

    # Concatenating relevant information into one Ensemble_list
    ENSEMBLE_LIST = []
    for param, id, mc in zip(PARAMS_LIST, PARAMS_ENSEMBLE["IDS"], PARAMS_ENSEMBLE["MODEL_CHECKPOINTS"]):
        ENSEMBLE_LIST.append({"PARAMS": param, "ID": id, "MODEL_CHECKPOINT": mc})

    ###################################
    # END OF: ENSEMBLE data setup #####
    ###################################

    return PARAMS_ENSEMBLE, ENSEMBLE_LIST, LABEL_COLUMNS, NAME
