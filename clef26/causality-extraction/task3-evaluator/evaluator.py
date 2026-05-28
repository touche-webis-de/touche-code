#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Literal

from sklearn.metrics import precision_score, recall_score, f1_score
import pandas as pd


def to_prototext(results: dict) -> str:
    out = ""
    for k, v in results.items():
        out += f'measure {{\n  key: "{k}"\n  value: "{v}"\n}}\n'
    return out


def main():
    parser = argparse.ArgumentParser(description='Evaluates classification using F1, Precision, and Recall')
    parser.add_argument("-p", "--predictions",
                        help="path to the dir holding the predictions (in a folder for each dataset/task)",
                        type=Path,
                        required=True)
    parser.add_argument("-t", "--truth",
                        help="path to the dir holding the true labels (in a folder for each dataset/task)",
                        type=Path,
                        required=True)
    parser.add_argument("-o", "--output", help="path to the dir to write the results to", required=True, type=Path)
    parser.add_argument("--index-field", help="The name for the index column (primary key)", default="index", type=str)
    parser.add_argument("--value-field",
                        help="The name for the column that contains the predicted spans",
                        default="label",
                        type=str)
    parser.add_argument("--agg", help="the aggregation strategy (micro, macro)", type=str, choices=["micro", "macro"], default="micro")
    args = parser.parse_args()

    truth_file = next(args.truth.glob("*.jsonl"))
    run_file = next(args.predictions.glob("*.jsonl"))

    df_truth = pd.read_json(truth_file, lines=True).set_index(args.index_field)[[args.value_field]]
    df_run = pd.read_json(run_file, lines=True).set_index(args.index_field)
    df_run = df_run[[args.value_field]].rename(columns={args.value_field: f"{args.value_field}_pred"})

    df = df_truth.join(df_run, how="left") # Potential bug: Left Join introduces NaN for entries that did not exist on the right

    y_true = df[args.value_field].tolist()
    y_pred = df[f"{args.value_field}_pred"].tolist()

    results = {
        "F1": f1_score(y_true, y_pred, average="macro"),
        "P": precision_score(y_true, y_pred, average="macro"),
        "R": recall_score(y_true, y_pred, average="macro"),
    }

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "evaluation.prototext").write_text(to_prototext(results))
    


if __name__ == "__main__":
    main()