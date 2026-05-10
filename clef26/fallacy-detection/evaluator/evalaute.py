#!/usr/bin/env python3
from pathlib import Path

import pandas as pd
from glob import glob
from tira.io_utils import to_prototext
import click

TASK_TO_EXPECTED_LABELS = {
    "fallacy_detection": set(["fallacy", "non-fallacy"]),
    "scheme_classification": set(["practical-internal", "practical-external", "epistemic-internal", "epistemic-external"]),
    "fallacy_classification": set(["authority", "black-white", "hasty_generalization", "natural", "population", "slippery_slope", "tradition", "worse_problems"]),
}
    

@click.command()
@click.option('--dataset', default='../data/task-1-fallacy-detection/touchefallacy_2026_test_task.jsonl', help='The dataset to run predictions on (can point to a local directory).')
@click.option('--run', type=Path, help='The file where predictions should be written to.')
@click.option('--task', type=str, required=True, help='The task on which this baseline runs.')
@click.option('--output', type=Path, required=True)
def main(dataset, output, task, run):
    truths = pd.read_json(glob(f"{dataset}/*.jsonl")[0], lines=True, orient="records")
    preds = pd.read_json(glob(f"{run}/*.jsonl")[0], lines=True, orient="records")
    required_ids = set(list(truths["id"].unique()))
    expected_labels = TASK_TO_EXPECTED_LABELS[task]
    actual_ids = set()
    predictions = 0

    for _, i in preds.iterrows():
        predictions += 1
        if "id" not in i or "label" not in i or "tag" not in i or "system_description" not in i:
            continue
        if i["id"] not in required_ids:
            continue
        if i["task"] != task:
            continue
        if i["label"] not in expected_labels:
            continue
        if i["tag"] not in ("base", "enhanced"):
            continue
        actual_ids.add(i["id"])

    results = {
        "predictions": len([i for i in actual_ids if i in required_ids]),
        "unexpected_predictions": predictions-len([i for i in actual_ids if i in required_ids]),
        "missing_predictions": len([i for i in required_ids if i not in actual_ids]),
    }
    print(results)

    with open(output / "evaluation.prototext", 'w') as f:
        f.write(to_prototext([results]))

if __name__ == "__main__":
    main()
