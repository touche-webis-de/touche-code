#!/usr/bin/env python3
import argparse
import math
from pathlib import Path
from typing import TypeVar

import pandas as pd


T = TypeVar("T")

def mean(values: list[T], default: T) -> T:
    return sum(values) / len(values) if values else default

def overlap(a: tuple[int, int], b: tuple[int, int]) -> float:
    """Computes the portion of the interval a that is overlapped by interval b"""
    if a[0] >= a[1]:
        return 0
    overlap = max(0, min(a[1], b[1]) - max(a[0], b[0]))
    return overlap / (a[1] - a[0])

def max_span_score(a: tuple[int, int], bs: list[tuple[int, int]]) -> tuple[float, int]:
    """
    Returns a tuple consisting of (1) the largest overlap of a with any span in bs and (2) the number of spans in bs
    with which a had any overlap.
    """
    scores = [overlap(a, b) for b in bs]
    return max(scores, default=0), sum(score > 0 for score in scores)

def compute_precision(truths: list[tuple[int, int]], predictions: list[tuple[int, int]]) -> float:
    """Computes the precision, i.e., the average largest overlap the prediction has with any truth span"""
    return mean([max_span_score(tup, truths)[0] for tup in predictions], default=0.0)

def compute_recall(truths: list[tuple[int, int]], predictions: list[tuple[int, int]]) -> float:
    """Computes the recall, i.e., the average largest overlap the truth spans has with any predicted span"""
    return mean([max_span_score(tup, predictions)[0] for tup in truths], default=0.0)

def compute_granularity(truths: list[tuple[int, int]], predictions: list[tuple[int, int]]) -> float:
    """
    From https://downloads.webis.de/publications/papers/potthast_2014c.pdf
    Penalizes multiple predicted spans matching the same ground-truth span.
    """
    results = (max_span_score(t, predictions) for t in truths)
    return mean([matches for score, matches in results if score > 0], default=0.0)

def compute_iou(truths: list[tuple[int, int]], predictions: list[tuple[int, int]]):
    set_a = {x for a in truths for x in range(a[0], a[1])}
    set_b = {x for b in predictions for x in range(b[0], b[1])}
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)

def compute_all_scores(truths: list[tuple[int, int]], predictions: list[tuple[int, int]]):
    precision = compute_precision(truths, predictions)
    recall = compute_recall(truths, predictions)
    granularity = compute_granularity(truths, predictions)
    iou = compute_iou(truths, predictions)

    # Standard F1
    if precision == 0 or recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    # Granularity-penalized F1
    if granularity == 0:
        f1_gran = f1
    else:
        f1_gran = f1 / math.log2(1 + granularity)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "granularity": granularity,
        "f1_gran": f1_gran,
        "intersection_over_union": iou,
    }


def to_prototext(results: dict) -> str:
    out = ""
    for k, v in results.items():
        out += f'measure {{\n  key: "{k}"\n  value: "{v}"\n}}\n'
    return out


def main():
    parser = argparse.ArgumentParser(description='A dummy evaluator that always outputs a score of 0')
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
                        default="spans",
                        type=str)
    args = parser.parse_args()

    truth_file = next(args.truth.glob("*.jsonl"))
    run_file = next(args.predictions.glob("*.jsonl"))

    df_truth = pd.read_json(truth_file, lines=True).set_index(args.index_field)[[args.value_field]]
    df_run = pd.read_json(run_file, lines=True).set_index(args.index_field)
    df_run = df_run[[args.value_field]].rename(columns={args.value_field: f"{args.value_field}_pred"})

    df = df_truth.join(df_run, how="left") # Potential bug: Left Join introduces NaN for entries that did not exist on the right

    scores = df.apply(lambda row: compute_all_scores(row[args.value_field], row[f"{args.value_field}_pred"]), axis=1)
    result = pd.DataFrame(list(scores)).mean().to_dict()

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "evaluation.prototext").write_text(to_prototext(result))


if __name__ == "__main__":
    main()