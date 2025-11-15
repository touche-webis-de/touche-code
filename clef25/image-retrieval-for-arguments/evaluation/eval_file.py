"""
NDCG Evaluation Pipeline
------------------------
This file loads annotation scores, loads retrieval/generation system runs,
computes NDCG@k per argument, averages them, and prints sorted results.

Main components:
- AnnotationLoader: loads annotator JSON files and converts answers to relevance scores.
- RunPreparation: loads JSONL retrieval/generation submissions into a standard structure.
- NDCGCalculator: computes NDCG@k for each system.

To run:
    python evaluate.py

Expected project structure:
    annotations_final/
        retrieval/*.json
        generation/*.json
    runs_submitted_dedup/
        retrieval/**.jsonl
        generation/**.jsonl

You must define `PROJECT_ROOT` in settings.py.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict
from tabulate import tabulate


# =======================================================
# AnnotationLoader
# ============================================s===========

class AnnotationLoader:
    """
    Loads annotation files and converts annotator judgments
    into relevance scores for (argumentId, imageId) pairs.
    """

    def __init__(self, annotation_dir: Path,
                 argument_id_key="argumentId",
                 image_id_key="imageId"):

        self.ARGUMENT_ID_KEY = argument_id_key
        self.IMAGE_ID_KEY = image_id_key
        self.all_annotation_dict = {}

        # Load all .json annotation files from directory
        for path in Path(annotation_dir).iterdir():
            if path.suffix == ".json":
                annotation_list = self.load_json(path)
                annotator_entry = self.build_single_annotator_dict(annotation_list)
                self.all_annotation_dict[annotator_entry["annotator"]] = annotator_entry["scores"]

        # Combine two annotators if available
        if len(self.all_annotation_dict) == 2:
            combined = self.build_combined_annotator_dict(self.all_annotation_dict)
            self.all_annotation_dict[combined["annotator"]] = combined["scores"]

    def load_json(self, path: Path):
        with open(path, "r") as f:
            return json.load(f)

    def annotator_score_to_int(self, answer: str):
        """
        Converts annotator label to numeric score.
        """
        mapping = {"no": 0, "partially agree": 1, "yes": 2}
        if answer not in mapping:
            raise ValueError(f"Invalid score: {answer}")
        return mapping[answer]

    def combine_two_scores(self, scores):
        """
        Combines two numeric scores using predefined rules.
        """
        if len(scores) != 2:
            raise ValueError("Expected exactly two annotation scores.")
        a, b = scores

        # All rules (from your original implementation)
        if a == 2 and b == 2:
            return 2
        if {a, b} == {1, 2}:
            return 2
        if {a, b} == {0, 2}:
            return 1
        if {a, b} == {0, 1}:
            return 1
        if a == 1 and b == 1:
            return 1
        if a == 0 and b == 0:
            return 0

        raise ValueError(f"Unexpected score combination: {a}, {b}")

    def build_single_annotator_dict(self, annotation_list):
        """
        Builds relevance dict for one annotator.
        """
        scores = {}
        tags = set()

        for entry in annotation_list:
            arg_id = entry[self.ARGUMENT_ID_KEY]
            img_id = entry[self.IMAGE_ID_KEY]

            answers = [self.annotator_score_to_int(a["answer"]) for a in entry["aspects"]]
            tags.update(str(a["annotatorTag"]).lower() for a in entry["aspects"])

            scores[(arg_id, img_id)] = self.combine_two_scores(answers)

        return {"annotator": " & ".join(sorted(tags)), "scores": scores}

    def build_combined_annotator_dict(self, annotator_dict):
        """
        Combines two annotator score dicts into a third dict.
        """
        if len(annotator_dict) != 2:
            raise AssertionError("Expected exactly two annotators.")

        annotator_names = sorted(annotator_dict.keys())
        combined_scores = {}

        # Union of all argument/image pairs
        all_pairs = set().union(*(annotator_dict[a].keys() for a in annotator_names))

        for pair in all_pairs:
            a, b = annotator_names
            score1 = annotator_dict[a].get(pair)
            score2 = annotator_dict[b].get(pair)

            if score1 is None or score2 is None:
                print(f"Warning: Missing scores for pair {pair}")
                continue

            combined_scores[pair] = self.combine_two_scores([score1, score2])

        return {
            "annotator": "&".join(annotator_names),
            "scores": combined_scores
        }


# =======================================================
# RunPreparation
# =======================================================

class RunPreparation:
    """
    Loads and structures system runs (retrieval or generation).
    """

    def __init__(self, file_list, mode="retrieval", dir_with_documents=None):
        self.mode = mode
        self.dir_with_documents = dir_with_documents
        self.prepared_runs = []

        for file_path in file_list:
            run = self.load_jsonl(file_path)
            team = os.path.basename(os.path.dirname(file_path))
            prepared = self.structure_run(run, team)

            # For generation only: adjust image_id as path
            if mode == "generation":
                directory = Path(file_path).parent
                for arg_id, items in prepared["run_dict"].items():
                    for item in items:
                        img = item["image_id"]
                        new_path = (directory / "image" / img).relative_to(self.dir_with_documents)
                        item["image_id"] = str(new_path)

            self.prepared_runs.append(prepared)

    def load_jsonl(self, path):
        with open(path, "r") as f:
            return [json.loads(line) for line in f if line.strip()]

    def structure_run(self, entries, team):
        """
        Converts JSONL records into grouped dict: {argument_id: [sorted submissions]}
        """
        groups = defaultdict(list)
        tags = set()

        for e in entries:
            groups[e["argument_id"]].append(e)
            tags.add(e.get("tag", "default"))

        # Sort each argument’s list by rank
        run_dict = {aid: sorted(vals, key=lambda x: x["rank"]) for aid, vals in groups.items()}
        run_tag = "&".join(sorted(tags))

        return {"team": team, "run_tag": run_tag, "run_dict": run_dict}


# =======================================================
# NDCGCalculator
# =======================================================

class NDCGCalculator:
    """
    Computes NDCG@k for each submission.
    """

    def __init__(self, relevance_scores, arg_ids_to_exclude=None,
                 argument_id_key="argument_id",
                 image_id_key="image_id"):

        self.relevance_scores = relevance_scores
        self.arg_ids_to_exclude = set(arg_ids_to_exclude or [])
        self.ARG_KEY = argument_id_key
        self.IMG_KEY = image_id_key

        self.top_ks = [1, 3, 5]
        self.all_runs_dict = {}
        self.used_tags = set()
        self.final_scores = []

    # ---------- Metrics ----------

    @staticmethod
    def dcg(rel, k):
        rel = np.asarray(rel[:k], dtype=float)
        return np.sum(rel / np.log2(np.arange(2, len(rel) + 2))) if rel.size else 0.0

    def ndcg(self, ideal, rel, k):
        dcg = self.dcg(rel, k)
        idcg = self.dcg(ideal, k)
        return dcg / idcg if idcg > 0 else 0.0

    # ---------- Evaluation ----------

    def do_evaluation(self, prepared_runs):
        """
        Computes NDCG for each run and stores results internally.
        """
        # Register runs
        for run in prepared_runs:
            combo = (run["team"], run["run_tag"])
            if combo in self.used_tags:
                print(f"Skipping duplicate: {combo}")
                continue
            self.used_tags.add(combo)
            self.all_runs_dict[combo] = run

        # Compute NDCG for each k
        for k in self.top_ks:
            for (team, tag), run_info in self.all_runs_dict.items():
                run_dict = run_info["run_dict"]
                scores_per_arg = []

                for arg_id, items in run_dict.items():
                    if arg_id in self.arg_ids_to_exclude:
                        continue

                    img_ids = [i[self.IMG_KEY] for i in items][:5]
                    rel_scores = []

                    for img in img_ids:
                        key = (arg_id, img)
                        if key not in self.relevance_scores:
                            raise ValueError(f"Missing relevance for {key}")
                        rel_scores.append(self.relevance_scores[key])

                    # construct ideal ranking
                    ideal = sorted(
                        [v for (a, _), v in self.relevance_scores.items() if a == arg_id],
                        reverse=True
                    )[:5]

                    if not ideal:
                        continue

                    ndcg_val = self.ndcg(ideal, rel_scores, k)
                    scores_per_arg.append(ndcg_val)

                if scores_per_arg:
                    mean_ndcg = np.mean(scores_per_arg)
                    self.final_scores.append({
                        "team": team,
                        "run_tag": tag,
                        "k": k,
                        "argument_id": "mean",
                        "ndcg": mean_ndcg
                    })

    def process_df(self):
        """Return pivoted dataframe with ndcg@k columns."""
        df = pd.DataFrame(
            s for s in self.final_scores if s["argument_id"] == "mean"
        )

        pivot = df.pivot(
            index=["team", "run_tag"],
            columns="k",
            values="ndcg"
        ).reset_index()

        pivot.columns = [
            f"ndcg@{col}" if isinstance(col, int) else col for col in pivot.columns
        ]
        return pivot


# =======================================================
# Utility functions
# =======================================================

def find_jsonl_files(directory):
    """Recursively find all .jsonl files."""
    return [
        os.path.join(root, f)
        for root, _, files in os.walk(directory)
        for f in files if f.endswith(".jsonl")
    ]


def pretty_sort_ndcg(df, sort_col="ndcg@5", as_latex=False, as_html=False):
    """Human-friendly output using tabulate or HTML or LaTeX."""
    df = df.sort_values(sort_col, ascending=False).reset_index(drop=True)
    df.index += 1
    df[df.select_dtypes(include=[float]).columns] = df.select_dtypes(
        include=[float]).round(4)

    if as_html:
        return df.to_html(index=True, border=1, justify="center")
    if as_latex:
        return df.to_latex(index=True, escape=False)
    return tabulate(df, headers="keys", tablefmt="grid")


def combine_dfs(df1, df2, df3):
    """Merge three annotator result tables."""
    df1 = df1.rename(columns={c: f"{c}_ann_1" for c in df1.columns if c.startswith("ndcg")})
    df2 = df2.rename(columns={c: f"{c}_ann_2" for c in df2.columns if c.startswith("ndcg")})
    df3 = df3.rename(columns={c: f"{c}_combined" for c in df3.columns if c.startswith("ndcg")})

    merged = df1.merge(df2, on=["run_tag", "team"]).merge(df3, on=["run_tag", "team"])
    merged = merged.reset_index(drop=True)
    merged[merged.select_dtypes(include=[float]).columns] = merged.select_dtypes(include=[float]).round(4)
    return merged


# =======================================================
# MAIN EXECUTION
# =======================================================

if __name__ == "__main__":

    # Arguments to exclude from evaluation
    IDS_TO_EXCLUDE = [
        "2-3", "4-1", "4-2", "4-3", "4-4",
        "8-3", "9-4", "13-3", "17-4", "21-6",
        "27-1", "27-3", "27-5"
    ]

    # ---- USER CONFIGURATION ----
    PATH_ANNOTATIONS_RETRIEVAL = "./annotations_final/retrieval"
    PATH_ANNOTATIONS_GENERATION = "./annotations_final/generation"

    PATH_RUNS_RETRIEVAL = "./runs_submitted_dedup/retrieval"
    PATH_RUNS_GENERATION = "./runs_submitted_dedup/generation"


    # ---------------- Retrieval evaluation ----------------

    retrieval_ann = AnnotationLoader(Path(PATH_ANNOTATIONS_RETRIEVAL)).all_annotation_dict
    retrieval_files = find_jsonl_files(PATH_RUNS_RETRIEVAL)
    retrieval_runs = RunPreparation(retrieval_files).prepared_runs

    calc = NDCGCalculator(retrieval_ann["max"], IDS_TO_EXCLUDE)
    calc.do_evaluation(retrieval_runs)
    max_df = calc.process_df()

    calc = NDCGCalculator(retrieval_ann["sharat"], IDS_TO_EXCLUDE)
    calc.do_evaluation(retrieval_runs)
    sharat_df = calc.process_df()

    calc = NDCGCalculator(retrieval_ann["max&sharat"], IDS_TO_EXCLUDE)
    calc.do_evaluation(retrieval_runs)
    combined_df = calc.process_df()

    print("\n=== Retrieval Ranking ===")
    print(pretty_sort_ndcg(combined_df, "ndcg@5", as_latex=True))

    merged_retrieval = combine_dfs(max_df, sharat_df, combined_df)

    # ---------------- Generation evaluation ----------------

    generation_ann = AnnotationLoader(Path(PATH_ANNOTATIONS_GENERATION)).all_annotation_dict
    generation_files = find_jsonl_files(PATH_RUNS_GENERATION)
    generation_runs = RunPreparation(
        generation_files, mode="generation",
        dir_with_documents= "runs_submitted_dedup/generation"
    ).prepared_runs

    calc = NDCGCalculator(generation_ann["max"], IDS_TO_EXCLUDE)
    calc.do_evaluation(generation_runs)
    max_g = calc.process_df()

    calc = NDCGCalculator(generation_ann["sharat"], IDS_TO_EXCLUDE)
    calc.do_evaluation(generation_runs)
    sharat_g = calc.process_df()

    calc = NDCGCalculator(generation_ann["max&sharat"], IDS_TO_EXCLUDE)
    calc.do_evaluation(generation_runs)
    combined_g = calc.process_df()

    print("\n=== Generation Ranking ===")
    print(pretty_sort_ndcg(combined_g, "ndcg@5", as_latex=True))
