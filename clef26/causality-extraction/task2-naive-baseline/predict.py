#!/usr/bin/env python3
from pathlib import Path

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='../task2-spot-check-dataset/inputs.jsonl', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "predictions.jsonl", type=Path, help='The file where predictions should be written to.')
def main(dataset, output):
    # Load the data
    tira = Client()
    df = tira.pd.inputs(dataset)

    # do the "predictions"; it always predicts the first half and the second half of the inputs to be events
    df['entity'] = df["text"].apply(lambda t: [[0, len(t)//2], [len(t)//2+1, len(t)-1]])

    # Set an identifier that names your approach
    df["tag"] = "naive"

    # Save the predictions
    df[["index", "entity", "tag"]].to_json(output / "predictions.jsonl", orient="records", lines=True)

if __name__ == "__main__":
    main()
