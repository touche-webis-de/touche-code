#!/usr/bin/env python3
import click
from tira.rest_api_client import Client
from pathlib import Path
from shutil import copytree
import json


@click.command()
@click.option("--task", type=click.Choice(["advertisement-in-retrieval-augmented-generation-2025"]), required=True, help="The task id in tira. See https://archive.tira.io/datasets?query=advertisement")
@click.option("--datasets", type=click.Choice(["ads-in-rag-task-1-generation-test-20250506-test", "ads-in-rag-task-1-generation-test-20250603-test"]), multiple=True, help="The dataset id in tira. See https://archive.tira.io/datasets?query=advertisement")
@click.option("--output", type=str, required=True, help="The output directory.")
def main(task, datasets, output):
    tira = Client()
    
    with open(f"{output}/submissions.jsonl", "w+") as f:
        for dataset in datasets:
            for _, submission in tira.submissions(task, dataset).iterrows():
                if submission["is_evaluation"]:
                    continue

                f.write(json.dumps(submission.to_dict()) + "\n")
                run_directory = tira.download_zip_to_cache_directory(task=task, dataset=dataset, team=submission["team"], run_id=submission["run_id"])
                copytree(Path(run_directory).parent, f"{output}/{submission['run_id']}")


if __name__ == '__main__':
    main()
