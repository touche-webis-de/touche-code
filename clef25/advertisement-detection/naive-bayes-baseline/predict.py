#!/usr/bin/env python3
from pathlib import Path

from joblib import load
from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='advertisement-in-retrieval-augmented-generation-2025/native-ads-2024-spot-check-20250414-training', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "predictions.jsonl", help='The file where predictions should be written to.')
@click.option('--threshold', default=0.5, help='The threshold at which the naive bayes probabilities are mapped to 1.')
def main(dataset, output, threshold):
    # Load the data
    tira = Client()
    df = tira.pd.inputs(dataset)

    # Load the model and make predictions
    model = load(Path(__file__).parent / "model.joblib")
    df['label'] = [1 if i[1] >= threshold else 0 for i in model.predict_proba(df["response"])]

    # Save the predictions
    df[["id", "label"]].to_json(output, orient="records", lines=True)

if __name__ == "__main__":
    main()
    