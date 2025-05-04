#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
from tqdm import tqdm

from tira.rest_api_client import Client
from tira.third_party_integrations import get_output_directory
import click

@click.command()
@click.option('--dataset', default='advertisement-in-retrieval-augmented-generation-2025/ads-in-rag-generation-spot-check-20250414-training', help='The dataset to run generations on (can point to a local directory).')
@click.option('--output', default=Path(get_output_directory(str(Path(__file__).parent))) / "generations.jsonl", help='The file where generated responses should be written to.')

def main(dataset, output):
    # Load the data
    tira = Client()
    df = tira.pd.inputs(dataset)

    out_data = []
    for i, row in tqdm(df.iterrows()):
        
        query_id = row["query"]["id"]
        query_text = row["query"]["text"]
        candidate = max(row["candidates"], key=lambda x:x["score"])

        for i, advertisement in enumerate(row["advertisements"]):
            ad = get_ad(advertisement)
            segment = candidate["doc"]["segment"]
            text = segment if ad == "" else " ".join([segment, ad, advertisement["qualities"]])
            item = advertisement["item"] if advertisement is not None else ''
            out_data.append([f"{query_id}-{i}", query_text, [candidate["docid"]], text, item, "baseline"])
    out_df = pd.DataFrame(out_data, columns=["id", "topic", "references", "response", "advertisement", "tag"])

    # Save the generations
    out_df.to_json(output, orient="records", lines=True)


def get_ad(advertisement):
    if advertisement is None:
        return ""
    formulations = [
        f"For those interested in {advertisement['qualities']}, consider looking at {advertisement['item']}."
    ]
    return formulations[0]

if __name__ == "__main__":
    main()
    