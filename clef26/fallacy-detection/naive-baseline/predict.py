#!/usr/bin/env python3
from pathlib import Path

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='../data/task-1-fallacy-detection/touchefallacy_2026_test_task.jsonl', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "predictions.jsonl", type=Path, help='The file where predictions should be written to.')
@click.option('--task', type=str, required=True, help='The task on which this baseline runs.')
@click.option('--predict', type=str, required=True, help='The naive prediction that this baseline will make for every input.')
def main(dataset, output, predict, task):
    # Load the data
    tira = Client()
    df = tira.pd.inputs(dataset)

    # do the "predictions"
    df['label'] = predict

    # Set an identifier that names your approach
    df["tag"] = "base"
    df["system_description"] = "A naive system"
    df["task"] = task

    # Save the predictions
    df[["id", "task", "label", "tag", "system_description"]].to_json(output, orient="records", lines=True)

if __name__ == "__main__":
    main()
