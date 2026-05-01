#!/usr/bin/env python3
from pathlib import Path

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='../task3-spot-check-dataset/inputs.jsonl', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "predictions.jsonl", type=Path, help='The file where predictions should be written to.')
@click.option('--predict', type=click.Choice(["0", "1", "2"]), default=0, help='The naive prediction that this baseline will make for every input.')
def main(dataset, output, predict):
    # Load the data
    tira = Client()
    df = tira.pd.inputs(dataset)

    # do the "predictions"
    df['label'] = predict

    # Set an identifier that names your approach
    df["tag"] = "naive"

    # Save the predictions
    df[["index", "label", "tag"]].to_json(output / "predictions.jsonl", orient="records", lines=True)

if __name__ == "__main__":
    main()
