#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import re
from tqdm import tqdm

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='advertisement-in-retrieval-augmented-generation-2026/ads-in-rag-task-2-span-prediction-spot-check-20260422-training', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "predictions.jsonl", help='The file where rewritten responses should be written to.')
def main(dataset, output):
    # Load the data
    tira = Client()

    df = tira.pd.inputs(dataset)

    # Detect the advertising text
    tqdm.pandas(desc="Predicting ad spans")
    predictions = df.progress_apply(get_last_two_sentence_spans, axis=1)
    predictions['tag'] = ['span-prediction-dummy-baseline'] * len(predictions.index)

    # Save the predictions
    predictions[["id", "spans", "tag"]].to_json(output, orient='records', lines=True)



def get_last_two_sentence_spans(row):
    """
    Returns character offsets (spans) of the last two sentences as [(start1, end1), (start2, end2)].
    """
    text = row["response"]

    # Regex to split sentences while keeping delimiters
    sentence_pattern = re.compile(r'[^.!?]*[.!?]')

    matches = list(sentence_pattern.finditer(text))

    # If fewer than 2 sentences, return whatever exists
    last_two = matches[-2:] if len(matches) >= 2 else matches

    # Extract (start, end) spans
    row["spans"] = [(m.start(), m.end()) for m in last_two]
    return row


if __name__ == "__main__":
    main()