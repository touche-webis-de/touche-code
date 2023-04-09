#!/usr/bin/env python3
import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description='This is a baseline for task 4 of Touche 2023.')

    parser.add_argument('--input', type=str, help='The input data (expected in tsv format).', required=True)
    parser.add_argument('--output', type=str, help='The output in tsv format.', required=True)

    return parser.parse_args()


def predict_label(instance):
    return 'In favor'


if __name__ == '__main__':
    args = parse_args()
    data = pd.read_csv(args.input, sep='\t', index_col=False)
    
    with open(args.output, 'w') as f:
        for _, i in data.iterrows():
            f.write(i['id'] + '\t' + predict_label(i) + '\n')

