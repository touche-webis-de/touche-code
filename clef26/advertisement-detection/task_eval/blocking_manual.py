import click
import pandas as pd
import time

from annotation_ui import AnnotationUI
from evaluator import Evaluator

class BlockingEvaluator(Evaluator):
    def __init__(self, dataset: str,
                 truth_file: str = None,
                 run_file: str = None,
                 run_id: str = None):
        super().__init__(dataset=dataset,
                         truth_file=truth_file,
                         run_file=run_file,
                         run_id=run_id)
        self.inputs = self.tira.pd.inputs(dataset)
        self.score_path = self.eval_dir / "scores_manual.json"

    def score_run(self):
        # Combine
        # 1. self.inputs to get the responses with ads and the queries
        # 2. self.truths to get the reference responses without ads
        # 3. self.df to get the blocked responses (Left join to keep all inputs)
        df = pd.merge(self.inputs, self.truths,
                      on="id",
                      how="inner",
                      suffixes=("_ad", "_reference"))
        df = (pd.merge(df, self.df,
                      on="id",
                      how="left")
              .rename(columns={"response": "response_blocked"}))

        # Collect evaluations
        ui = AnnotationUI(df=df, eval_path=self.eval_dir / "element_scores_manual.jsonl")
        ui.render()
        while not ui.is_finished():
            time.sleep(1)
            continue

        # Get the scores per row and add meta information
        df_eval = ui.get_results()
        df_eval = pd.merge(df_eval, df[["id", "response_ad", "response_blocked","response_reference", "spans"]],
                           on="id").rename(columns={
            "response_ad": "ad_response",
            "response_blocked": "blocked_response",
            "response_reference": "reference_response",
        })

        # Save the detailed evaluations
        output_path = self.eval_dir / "element_scores_manual.jsonl"
        df_eval.to_json(output_path, orient="records", lines=True)
        print(f"Saved the detailed results to {output_path}")

        # Get the aggregate scores
        self.result = {
            "correctness": float(df_eval["correctness"].mean()),
            "fluency": float(df_eval["fluency"].mean()),
            "relevance": float(df_eval["relevance"].mean()),
        }


@click.command("Touché Evaluation - Ad Blocking (Manual Evaluation)")
@click.argument('dataset', default='ads-in-rag-task-3-blocking-spot-check-20260424-training', type=str)
@click.option('--truth_file', type=str, help='Path to a local truth_file. If not set, the truths from TIRA will be used')
@click.option('--run_file', type=str, help='Path to a local run file.')
@click.option('--run_id', type=str, help='ID used to identify the run.')
def main(dataset: str,
        truth_file: str = None,
        run_file: str = None,
        run_id: str = None):
    evaluator = BlockingEvaluator(dataset=dataset,
                                  truth_file=truth_file,
                                  run_file=run_file,
                                  run_id=run_id)
    evaluator.evaluate()

if __name__ == "__main__":
    main()