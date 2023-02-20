import sys

from models.interface_modules.transformer_local import (download_model_data)
from models.interface_modules.load_ensemble_list import (load_ensemble_list)


def main(model_dir: str, dataset_dir: str):

    _, ENSEMBLE_LIST, _, _ = load_ensemble_list(model_dir=model_dir, dataset_dir=dataset_dir, verbose=True)

    downloaded_models = []
    for idx, elem in enumerate(ENSEMBLE_LIST):
        PARAMS = elem["PARAMS"]
        source_path = PARAMS['MODEL_PATH']
        if source_path not in downloaded_models:
            download_model_data(source_path)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) != 2:
        sys.exit(2)

    model_dir = arguments[0]
    dataset_dir = arguments[1]

    main(model_dir=model_dir, dataset_dir=dataset_dir)
