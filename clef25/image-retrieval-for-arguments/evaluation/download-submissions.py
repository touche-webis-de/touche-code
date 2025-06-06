#!/usr/bin/env python3
import click
from tira.rest_api_client import Client
from pathlib import Path
from tqdm import tqdm
import shutil
import json

def submissions(tira, task, dataset):
    for _, submission in tira.submissions(task, dataset).iterrows():
        if submission["is_evaluation"]:
            continue
        yield submission

@click.command()
@click.option("--task", type=click.Choice(["touche-task-3"]), required=True, help="The task id in tira. See https://archive.tira.io/datasets?query=touche")
@click.option("--datasets", type=click.Choice(["main-2025-20241213-training"]), multiple=True, help="The dataset id in tira. See https://archive.tira.io/datasets?query=touche")
def main(task, datasets):
    tira = Client()
    results = []
    repo_to_public = {}
    with open("runs/submissions.jsonl", "w") as f:
        for dataset in datasets:
            for submission in tqdm(list(submissions(tira, task, dataset)), dataset):
                f.write(json.dumps(submission.to_dict()) + '\n')
                run_directory = tira.download_zip_to_cache_directory(task=task, dataset=dataset, team=submission["team"], run_id=submission["run_id"])
                shutil.copytree(Path(run_directory).parent, Path("runs") / Path(run_directory).parent.name)

if __name__ == '__main__':
    main()
