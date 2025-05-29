#!/usr/bin/env python3
import click
from tira.rest_api_client import Client
from pathlib import Path
from collections import defaultdict


@click.command()
@click.option("--task", type=click.Choice(["ideology-and-power-identification-in-parliamentary-debates-2025"]), required=True, help="The task id in tira. See https://archive.tira.io/datasets?query=ideology-and-power")
@click.option("--datasets", type=click.Choice(["ideology-and-power-identification-20250504-test"]), multiple=True, help="The dataset id in tira. See https://archive.tira.io/datasets?query=ideology-and-power")
@click.option("--output", type=str, required=True, help="The output directory.")
def main(task, datasets, output):
    tira = Client()
    to_review = defaultdict(lambda: set())

    for dataset in datasets:
        for _, submission in tira.submissions(task, dataset).iterrows():
            run_directory = tira.download_zip_to_cache_directory(task=task, dataset=dataset, team=submission["team"], run_id=submission["run_id"])


if __name__ == '__main__':
    main()
