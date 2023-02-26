import pickle
import os


def load_ensemble_list(model_dir: str, threshold: float = 0.26, verbose: bool = False):

    if not model_dir.endswith(os.path.sep):
        model_dir += os.path.sep

    #####################################
    # START OF: ENSEMBLE data setup #####
    #####################################

    PARAMS_ENSEMBLE = {
        "MODEL_CHECKPOINTS": [os.path.join(model_dir, file) for file in os.listdir(model_dir) if file.endswith(".ckpt")],
        "DESCRIPTION": "SERVER",
        "MAX_THRESHOLD_METRIC": "custom",
        "ENSEMBLE": "EN",
        "ENSEMBLE_THRESHOLD": threshold,
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

    if len(PARAMS_ENSEMBLE['MODEL_CHECKPOINTS']) == 0:
        raise RuntimeError('No model checkpoints found in directory.')

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
