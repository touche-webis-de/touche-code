#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='advertisement-in-retrieval-augmented-generation-2026/ads-in-rag-task-3-blocking-spot-check-20260417-training', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "generations.jsonl", help='The file where rewritten responses should be written to.')
def main(dataset, output):
    # Load the data
    tira = Client()

    df = tira.pd.inputs(dataset)

    # Remove the advertising text
    tqdm.pandas(desc="Removing advertisements")
    generations = df.progress_apply(remove_ad_span, axis=1)
    generations['tag'] = ['removal-baseline'] * len(generations.index)

    # Save the rewritten responses
    generations[["id", "response", "tag"]].to_json(output, orient='records', lines=True)


def remove_ad_span(row: pd.Series):
    response = row["response"]
    spans = row["spans"]

    offset = 0
    for start_idx, end_idx in spans:
        start = response[:start_idx - offset]
        end = response[end_idx - offset:]

        if start.endswith(" "):
            start = start[:-1]
            offset += 1

        if not end.startswith(" "):
            end = f" {end}"
            offset -= 1

        response = start + end

        offset += (end_idx - start_idx)

    row["response"] = response
    return row


if __name__ == "__main__":
    main()