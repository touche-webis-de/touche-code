import click
from sklearn.metrics import recall_score, precision_score

from evaluator import Evaluator

class DetectionEvaluator(Evaluator):
    def __init__(self, dataset: str,
                 truth_file: str = None,
                 run_file: str = None,
                 run_id: str = None):
        super().__init__(dataset=dataset,
                         truth_file=truth_file,
                         run_file=run_file,
                         run_id=run_id)

    def score_run(self):
        y_true, y_pred = self.truths["label"], self.df["label"]

        p = precision_score(y_true=y_true, y_pred=y_pred)
        r = recall_score(y_true=y_true, y_pred=y_pred)

        if p * r == 0:
            f1 = 0
        else:
            f1 = 2*p*r/(p+r)

        self.result = {"precision": p, "recall": r, "f1": f1}

@click.command("Touché Evaluation - Ad Detection")
@click.argument('dataset', default='ads-in-rag-task-1-detection-spot-check-20260422-training', type=str)
@click.option('--truth_file', type=str, help='Path to a local truth_file. If not set, the truths from TIRA will be used')
@click.option('--run_file', type=str, help='Path to a local run file.')
@click.option('--run_id', type=str, help='ID used to identify the run.')
def evaluate(dataset: str,
             truth_file: str = None,
             run_file: str = None,
             run_id: str = None):
    evaluator = DetectionEvaluator(dataset=dataset,
                                   truth_file=truth_file,
                                   run_file=run_file,
                                   run_id=run_id)
    evaluator.evaluate()


if __name__ == "__main__":
    evaluate()