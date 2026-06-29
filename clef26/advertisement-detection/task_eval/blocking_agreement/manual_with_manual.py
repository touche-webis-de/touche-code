"""
Compute Krippendorff's alpha inter-annotator agreement for manual annotations
in a directory. Each file is treated as one annotator; annotations are matched
by their 'id' field. Reports alpha per dimension (relevance, correctness, fluency).

Usage:
    python manual_with_manual.py <directory>
"""

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import krippendorff
import numpy as np

from utils import DIMENSIONS, load_annotations


def build_reliability_matrix(
    annotators: dict[str, dict[str, dict]], dimension: str
) -> tuple[np.ndarray, list[str]]:
    """
    Build a reliability data matrix (annotators x items) for one dimension.
    Missing values become np.nan.
    Returns (matrix, ordered_item_ids).
    """
    all_ids = sorted({item_id for items in annotators.values() for item_id in items})
    names = list(annotators.keys())
    matrix = np.full((len(names), len(all_ids)), np.nan)
    for r, name in enumerate(names):
        for c, item_id in enumerate(all_ids):
            value = annotators[name].get(item_id, {}).get(dimension)
            if value is not None:
                matrix[r, c] = value
    return matrix, all_ids


def compute_alpha(annotators: dict[str, dict[str, dict]], dimension: str) -> tuple[float | None, int]:
    """Return (alpha, n_items) for the given annotators and dimension, or (None, 0) if insufficient data."""
    matrix, _ = build_reliability_matrix(annotators, dimension)
    mask = np.sum(~np.isnan(matrix), axis=0) >= 2
    matrix = matrix[:, mask]
    if matrix.size == 0:
        return None, 0
    alpha = krippendorff.alpha(reliability_data=matrix, level_of_measurement="ordinal")
    return alpha, int(mask.sum())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, help="Directory containing JSONL annotation files")
    args = parser.parse_args()

    if not args.directory.is_dir():
        sys.exit(f"Error: {args.directory} is not a directory")

    annotators = load_annotations(args.directory)

    if len(annotators) < 2:
        sys.exit(f"Error: need at least 2 annotator files, found {len(annotators)}")

    files = list(annotators.keys())
    names = [k.replace("element_scores_manual_", "").replace(".jsonl", "") for k in files]

    print(f"Annotators ({len(annotators)}):")
    for name, items in annotators.items():
        print(f"  {name}: {len(items)} items")
    print()

    results = {"overall": {}, "pairwise": {}}

    # Overall agreement across all annotators
    print("=== Overall agreement ===")
    for dim in DIMENSIONS:
        alpha, n = compute_alpha(annotators, dim)
        if alpha is None:
            print(f"  {dim}: no items with >= 2 annotations")
        else:
            print(f"  {dim}: alpha = {alpha:.4f}  ({n} items)")
            results["overall"][dim] = {"alpha": alpha, "n_items": n}
    print()

    # Pairwise agreement for each annotator pair
    print("=== Pairwise agreement ===")
    for a, b in combinations(files, 2):
        pair_annotators = {a: annotators[a], b: annotators[b]}
        name_a = names[files.index(a)]
        name_b = names[files.index(b)]

        label = f"{name_a} vs {name_b}"
        print(f"  {label}")
        pair_results = {}
        for dim in DIMENSIONS:
            alpha, n = compute_alpha(pair_annotators, dim)
            if alpha is None:
                print(f"    {dim}: no shared items")
            else:
                print(f"    {dim}: alpha = {alpha:.4f}  ({n} items)")
                pair_results[dim] = {"alpha": alpha, "n_items": n}
        results["pairwise"][label] = pair_results
        print()

    results["annotators"] = names
    output_path = args.directory / "agreement_krippendorffs_alpha_manual.json"
    with output_path.open("w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved agreement results to {output_path}")

if __name__ == "__main__":
    main()
