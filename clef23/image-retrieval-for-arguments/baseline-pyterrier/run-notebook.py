#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(description='Run Jupyter Notebook in TIRA with runnb.')

    parser.add_argument('--input', type=str, help='The directory that contains the input data (this directory is expected to contain a queries.jsonl and a documents.jsonl file).', required=True)
    parser.add_argument('--notebook', type=str, help='The notebook to execute.', required=True)
    parser.add_argument('--output', type=str, help='The resulting run.txt will be stored in this directory.', required=True)
    parser.add_argument('--local-dry-run', type=bool, help='Should the notebook be executed with docker as it would be in TIRA?', default=False, required=False)
    parser.add_argument('--enable-network-in-dry-run', type=bool, help='If the notebook is executed in local-dry-run, should the internet connection be removed? TIRA disables the internet connection (besides chatnoir.eu) to ensure that the software is fully installed in the image.', default=False, required=False)
    parser.add_argument('--image-for-dry-run', type=str, help='The docker image that is to be executed in the dry-run.', default='webis/tira-touche23-task-3-pyterrier-baseline:0.0.1', required=False)

    return parser.parse_args()


def main(args):
    os.environ['TIRA_INPUT_DIRECTORY'] = args.input
    os.environ['TIRA_OUTPUT_DIRECTORY'] = args.output

    command = f'runnb --allow-not-trusted {args.notebook}'
    
    if args.local_dry_run:
        network = '' if args.enable_network_in_dry_run else '--network=none'
        command = f'docker run --rm -ti {network} -v {args.input}:/input-in-container -v {args.output}:/output-in-container {args.image_for_dry_run} /workspace/run-notebook.py --notebook {args.notebook} --input /input-in-container --output /output-in-container'
        print(f'Execute dry run in docker. The command is:\n\n\t{command}\n\n')
    
    subprocess.check_call(command, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main(parse_args())

