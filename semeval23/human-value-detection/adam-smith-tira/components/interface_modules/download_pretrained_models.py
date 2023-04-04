import sys

from components.interface_modules.transformer_local import (download_model_data)


def main(model_dir_source: str):

    with open(model_dir_source, 'r') as f:
        lines = f.readlines()

    for line in lines:
        source_path = line.strip()
        download_model_data(source_path)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        sys.exit(2)

    model_dir_source = arguments[0]

    main(model_dir_source=model_dir_source)
