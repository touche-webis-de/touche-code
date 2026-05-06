#!/usr/bin/env python3

import os
from pathlib import Path
import pandas as pd
import math
from tqdm import tqdm


def load_jsonl(path: Path):
    return pd.read_json(path, lines=True)


class ElementwiseEval:
    def __init__(self, spans, spans_pred):
        self.spans = spans or []
        self.spans_pred = spans_pred or []

    def overlap(self, a, b):
        if a[0] == a[1]:
            return 0
        if a == b:
            return 1.0
        set_a = set(range(a[0], a[1]))
        set_b = set(range(b[0], b[1]))
        return len(set_a & set_b) / len(set_a)

    def max_span_score(self, tup_a, tuples_b):
        max_score = 0
        num_matches = 0
        for tup_b in tuples_b:
            score = self.overlap(tup_a, tup_b)
            max_score = max(max_score, score)
            if score > 0:
                num_matches += 1
        return max_score, num_matches

    def compute_precision(self):
        if not self.spans_pred:
            return 0.0

        p_sum = 0.0
        for tup in self.spans_pred:
            if tup in self.spans:
                p_sum += 1.0
            else:
                p_sum += self.max_span_score(tup, self.spans)[0]

        return p_sum / len(self.spans_pred)

    def compute_recall(self):
        if not self.spans:
            return 0.0

        r_sum = 0.0
        for tup in self.spans:
            if tup in self.spans_pred:
                r_sum += 1.0
            else:
                r_sum += self.max_span_score(tup, self.spans_pred)[0]

        return r_sum / len(self.spans)

    def compute_granularity(self):
        """
        From Potthast et al. (2014):
        Penalizes multiple predicted spans matching the same ground-truth span.
        """
        if not self.spans:
            return 0.0

        card_S_R = 0.0
        sum_R_S = 0.0

        for tup in self.spans:
            max_score, num_matches = self.max_span_score(tup, self.spans_pred)
            if max_score > 0:
                card_S_R += 1
                sum_R_S += num_matches

        if card_S_R == 0:
            return 0.0

        return sum_R_S / card_S_R

    def compute_iou(self):
        set_a = set()
        set_b = set()

        for a in self.spans:
            set_a |= set(range(a[0], a[1]))
        for b in self.spans_pred:
            set_b |= set(range(b[0], b[1]))

        union = set_a | set_b
        if not union:
            return 0.0

        return len(set_a & set_b) / len(union)

    def score(self):
        precision = self.compute_precision()
        recall = self.compute_recall()
        granularity = self.compute_granularity()
        iou = self.compute_iou()

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
    input_dataset = Path(os.environ["inputDataset"])
    input_run = Path(os.environ["inputRun"])
    output_dir = Path(os.environ["outputDir"])

    output_dir.mkdir(parents=True, exist_ok=True)

    truth_file = list(input_dataset.glob("*.jsonl"))[0]
    run_file = list(input_run.glob("*.jsonl"))[0]

    df_truth = load_jsonl(truth_file)
    df_run = load_jsonl(run_file)

    df = pd.merge(
        df_truth[["id", "spans"]],
        df_run[["id", "spans"]],
        on="id",
        how="left",
        suffixes=("", "_pred"),
    )

    tqdm.pandas()

    df_scores = df.progress_apply(
        lambda row: ElementwiseEval(
            row["spans"], row["spans_pred"]
        ).score(),
        axis=1,
    )

    df_scores = pd.DataFrame(list(df_scores))

    result = df_scores.mean().to_dict()

    # Write prototext
    with open(output_dir / "evaluation.prototext", "w") as f:
        f.write(to_prototext(result))


if __name__ == "__main__":
    main()