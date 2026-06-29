"""
Compare automated LLM annotations (continuous, 0-1) against manual annotations
(ordinal integers) using Kendall's tau-b per dimension.

Kendall's tau-b is chosen because:
- It measures the *strength* of monotonic agreement between the two scales,
  producing an interpretable coefficient in [-1, 1].
- It is rank-based and non-parametric, so it makes no distributional assumptions.
- Tau-b (vs tau-a) corrects for ties, which are abundant in ordinal data.

For each manual annotator the script reports tau-b and its p-value per dimension.

Usage:
    python manual_with_llm.py <directory>
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau

from utils import DIMENSIONS, load_annotations


def load_llm_annotations(directory: Path) -> dict[str, dict]:
    """Return {item_id: {dimension: value}} for the single LLM annotation file."""
    path = directory / "element_scores_llm.jsonl"
    if not path.exists():
        sys.exit(f"Error: LLM annotation file not found: {path}")
    items = {}
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            item_id = record["id"]
            items[item_id] = {dim: record[dim] for dim in DIMENSIONS if dim in record}
    return items


def paired_scores(
    manual: dict[str, dict],
    llm: dict[str, dict],
    dimension: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Return aligned (manual_scores, llm_scores) arrays for items present in both."""
    shared_ids = sorted(set(manual) & set(llm))
    manual_vals, llm_vals = [], []
    for item_id in shared_ids:
        m = manual[item_id].get(dimension)
        l = llm[item_id].get(dimension)
        if m is not None and l is not None:
            manual_vals.append(m)
            llm_vals.append(l)
    return np.array(manual_vals), np.array(llm_vals)


def compute_tau(
    manual: dict[str, dict],
    llm: dict[str, dict],
    dimension: str,
) -> tuple[float | None, float | None, int]:
    """Return (tau_b, p_value, n) or (None, None, 0) when there are too few pairs."""
    m, l = paired_scores(manual, llm, dimension)
    if len(m) < 3:
        return None, None, len(m)
    result = kendalltau(m, l, variant="b")
    return result.statistic, result.pvalue, len(m)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing JSONL annotation files")
    args = parser.parse_args()

    if not args.directory.is_dir():
        sys.exit(f"Error: {args.directory} is not a directory")

    manual_annotators = load_annotations(args.directory)
    if not manual_annotators:
        sys.exit("Error: no manual annotation files found (element_scores_manual_*.jsonl)")

    llm = load_llm_annotations(args.directory)

    annotator_names = {
        fname: fname.replace("element_scores_manual_", "").replace(".jsonl", "")
        for fname in manual_annotators
    }

    print(f"Manual annotators ({len(manual_annotators)}):")
    for fname, items in manual_annotators.items():
        print(f"  {annotator_names[fname]}: {len(items)} items")
    print(f"LLM annotations: {len(llm)} items")
    print()

    results = {}

    def _print_and_store(label: str, manual: dict[str, dict]) -> dict:
        row = {}
        print(f"  {label}")
        for dim in DIMENSIONS:
            tau, p, n = compute_tau(manual, llm, dim)
            if tau is None:
                print(f"    {dim}: insufficient paired items ({n})")
            else:
                stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
                print(f"    {dim}: tau-b = {tau:+.4f},  p = {p:.4f}{stars}  ({n} items)")
                row[dim] = {"tau_b": tau, "p_value": p, "n_items": n}
        return row

    print("=== Kendall's tau-b: each manual annotator vs LLM ===")
    for fname, items in manual_annotators.items():
        name = annotator_names[fname]
        results[name] = _print_and_store(name, items)
    print()

    output_path = args.directory / "agreement_kendalls_tau_b_llm.json"
    with output_path.open("w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {output_path}")


if __name__ == "__main__":
    main()
