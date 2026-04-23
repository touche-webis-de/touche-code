import click
import math
import pandas as pd
from tqdm import tqdm

from evaluator import Evaluator


class SpanPredictionEvaluator(Evaluator):
    def __init__(self, dataset: str,
                 truth_file: str = None,
                 run_file: str = None,
                 run_id: str = None):
        super().__init__(dataset=dataset,
                         truth_file=truth_file,
                         run_file=run_file,
                         run_id=run_id)

    def score_run(self):
        # Evaluate each element separately
        df = pd.merge(self.truths[["id", "spans"]], self.df[["id", "spans"]],
                      on="id",
                      how="left",
                      suffixes=["", "_pred"])

        tqdm.pandas(desc="Scoring span predictions")
        df_eval = df.progress_apply(self.score_element, axis=1)

        # Save the detailed evaluations
        output_path = self.eval_dir / "element_scores.jsonl"
        df_eval.to_json(output_path, orient="records", lines=True)
        print(f"Saved the detailed results to {output_path}")

        # Calculate the macro averages as the result
        self.result = df_eval.drop(columns=["id", "granularity"]).mean().to_dict()


    @staticmethod
    def score_element(row: pd.Series):
        element_eval = ElementwiseEval(spans=row["spans"], spans_pred=row["spans_pred"])
        return pd.Series({"id": row["id"], **element_eval.score()})


# TODO: Handle empty spans_pred
class ElementwiseEval:
    def __init__(self, spans: list[tuple[int, int]], spans_pred: list[tuple[int, int]]):
        self.spans = spans
        self.spans_pred = spans_pred

        # Initialize metrics
        self.precision = None
        self.recall = None
        self.f1 = None
        self.granularity = None
        self.f1_gran = None
        self.iou = None

    def score(self):
        self.set_precision()
        self.set_recall()
        self.set_granularity()
        self.set_intersection_over_union()

        if self.precision == 0 or self.recall == 0:
            self.f1 = 0
        else:
            self.f1 = 2 * self.precision * self.recall / (self.precision + self.recall)

        if self.granularity == 0:
            self.f1_gran = self.f1
        else:
            self.f1_gran = self.f1 / math.log(1 + self.granularity, 2)

        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "granularity": self.granularity,
            "f1_gran": self.f1_gran,
            "intersection_over_union": self.iou
        }

    def set_precision(self):
        p_sum = 0.0
        if not isinstance(self.spans_pred, list):
            self.precision = p_sum
            return

        for tup in self.spans_pred:
            if tup in self.spans:
                p_sum += 1.0
            else:
                max_score, _ = self.max_span_score(tup_a=tup, tuples_b=self.spans)
                p_sum += max_score

        # Handle cases with no predictions (p_sum will be 0 -> Precision is zero)
        self.precision = p_sum / max(1, len(self.spans_pred))

    def set_recall(self):
        r_sum = 0.0
        if not isinstance(self.spans_pred, list):
            self.recall = r_sum
            return
        
        for tup in self.spans:
            if tup in self.spans_pred:
                r_sum += 1.0
            else:
                max_score, _ = self.max_span_score(tup_a=tup, tuples_b=self.spans_pred)
                r_sum += max_score

        self.recall = r_sum / len(self.spans)

    @staticmethod
    def max_span_score(tup_a: tuple[int, int], tuples_b: list[tuple[int, int]]):
        """
        Computes the maximum score between the input tuple A and all candidates from B.
        Additionally, report the number of tuples in B that matched with A

        :param tup_a:       Tuple which to compare against a list of candidates
        :param tuples_b:    List of candidate tuples
        :return:
            - The maximum score between the input tuple A and all candidates
            - The number of tuples in B that matched with A
        """
        max_score = 0
        num_matches = 0

        for tup_b in tuples_b:
            score = overlap(tup_a, tup_b)
            max_score = max(max_score, score)
            if score > 0:
                num_matches += 1

        return max_score, num_matches

    def set_granularity(self):
        """
        Granularity measure from https://downloads.webis.de/publications/papers/potthast_2014c.pdf
        Penalize multiple predicted spans matching the same ground truth span.
        """
        card_S_R = 0.0
        sum_R_S = 0.0
        for tup in self.spans:
            max_score, num_matches = self.max_span_score(tup_a=tup, tuples_b=self.spans_pred)
            if max_score > 0:
                card_S_R += 1
                sum_R_S += num_matches
        if card_S_R == 0:
            self.granularity = 0
        else:
            self.granularity = sum_R_S / card_S_R

    def set_intersection_over_union(self):
        """
        Calculate the intersection over union (IoU) of all ground truth and character spans.
        """
        set_a = set()
        set_b = set()

        for tup_a in self.spans:
            set_a = set_a | set(range(tup_a[0], tup_a[1]))

        for tup_b in self.spans_pred:
            set_b = set_b | set(range(tup_b[0], tup_b[1]))

        self.iou = len(set_a & set_b) / len(set_a | set_b)


def overlap(tup_a, tup_b):
    """
    Measuring overlap between character offset tuples.
    Tuple A is the target that tuple B aims at.
    """
    if tup_a[0] == tup_a[1]:
        return None

    if tup_a == tup_b:
        return 1.0

    set_a = set(range(tup_a[0], tup_a[1]))


    set_b = set(range(tup_b[0], tup_b[1]))
    return len(set_a & set_b) / len(set_a)


@click.command("Touché Evaluation - Ad Span Prediction")
@click.argument('dataset', default='ads-in-rag-task-2-span-prediction-spot-check-20260422-training', type=str)
@click.option('--truth_file', type=str, help='Path to a local truth_file. If not set, the truths from TIRA will be used')
@click.option('--run_file', type=str, help='Path to a local run file.')
@click.option('--run_id', type=str, help='ID used to identify the run.')
def evaluate(dataset: str,
             truth_file: str = None,
             run_file: str = None,
             run_id: str = None):
    evaluator = SpanPredictionEvaluator(dataset=dataset,
                                        truth_file=truth_file,
                                        run_file=run_file,
                                        run_id=run_id)
    evaluator.evaluate()


if __name__ == "__main__":
    evaluate()