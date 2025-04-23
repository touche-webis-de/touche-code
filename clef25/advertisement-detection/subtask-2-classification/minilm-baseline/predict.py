#!/usr/bin/env python3
from pathlib import Path
from model_utils import SBertModel

from joblib import load
from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='advertisement-in-retrieval-augmented-generation-2025/native-ads-2024-spot-check-20250414-training', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "predictions.jsonl", help='The file where predictions should be written to.')
def main(dataset, output):
    # Load the data
    tira = Client()
    df = tira.pd.inputs(dataset)

    # Load the model and make predictions
    model = SBertModel(model_name="all-MiniLM-L6-v2", input_run=df)
    predictions = model.make_predictions()
    predictions['tag'] = ['minilm-baseline'] * len(predictions.index)

    # Save the predictions
    predictions.to_json(output, orient='records', lines=True)


if __name__ == "__main__":
    main()
    