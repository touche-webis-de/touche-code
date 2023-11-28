import argparse
import json
import os
import sys
from typing import Union

from huggingface_hub import hf_hub_download
from requests import HTTPError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--download-file', required=True)
    parser.add_argument('-t', '--token', required=False, default=None)

    return parser.parse_args()


def download_model_files(download_file: str, token: Union[str, None] = None):
    if not os.path.exists(download_file):
        sys.exit(-1)

    local_dir = os.path.dirname(download_file)

    with open(download_file, 'r') as json_file:
        json_list = [json.loads(json_line) for json_line in json_file.read().splitlines()]

    for hub_instance in json_list:
        if 'repo_id' not in hub_instance.keys() or not isinstance(hub_instance['repo_id'], str):

            continue
        if 'files' not in hub_instance.keys() or not isinstance(hub_instance['files'], list):

            continue
        repo_id = hub_instance['repo_id']
        files = hub_instance['files']

        for file_ref in files:
            if not isinstance(file_ref, dict):

                continue
            if 'source' not in file_ref.keys() or not isinstance(file_ref['source'], str):
                continue
            source_path = file_ref['source']
            destination_path = None
            if 'destination' in file_ref.keys() and isinstance(file_ref['destination'], str):
                destination_path = os.path.join(local_dir, file_ref['destination'])

            try:
                local_path = hf_hub_download(
                    repo_id=repo_id,
                    filename=source_path,
                    local_dir=local_dir,
                    local_dir_use_symlinks=False,
                    token=token
                )
            except HTTPError as he:
                sys.exit(str(he))

            if destination_path is not None and not os.path.exists(destination_path):
                os.rename(local_path, destination_path)


if __name__ == '__main__':
    args = parse_args()
    download_model_files(download_file=args.download_file, token=args.token)
