import click
from deepeval.evaluate import DisplayConfig
from deepeval.evaluate.types import EvaluationResult
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.models import GPTModel
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import evaluate
import pandas as pd
from typing import Any

from evaluator import Evaluator

MODEL = "gpt-5.4-mini"

class BlockingEvaluatorLLM(Evaluator):
    def __init__(self, dataset: str,
                 truth_file: str = None,
                 run_file: str = None,
                 run_id: str = None):
        super().__init__(dataset=dataset,
                         truth_file=truth_file,
                         run_file=run_file,
                         run_id=run_id)
        self.inputs = self.tira.pd.inputs(dataset)

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

        # Score the results
        deepeval_scorer = DeepevalScorer(df=df)
        deepeval_scorer.set_non_verbose_display_config()
        deepeval_scorer.score()

        # Get the scores per row
        df_eval = deepeval_scorer.df_results
        df_eval["ad_response"] = df["response_ad"]
        df_eval["spans"] = df["spans"]
        df_eval["response_blocked"] = df["response_blocked"]
        df_eval["response_reference"] = df["response_reference"]

        # Save the detailed evaluations
        output_path = self.eval_dir / "element_scores.jsonl"
        df_eval.to_json(output_path, orient="records", lines=True)
        print(f"Saved the detailed results to {output_path}")

        # Get the aggregate scores
        self.result = {
            "correctness": float(deepeval_scorer.correctness),
            "fluency": float(deepeval_scorer.fluency),
            "relevance": float(deepeval_scorer.relevance),
        }


class DeepevalScorer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.model = GPTModel(model=MODEL)
        self.test_cases = []
        self.create_test_cases()

        self.metrics = []
        self.set_create_metrics()

        # Initialize evaluation variables
        self.results = []
        self.df_results_detailed = pd.DataFrame()
        self.df_results = pd.DataFrame()
        self.display_config = DisplayConfig()

        # Initialize scores (averages)
        self.correctness = None
        self.fluency = None
        self.relevance = None

    def create_test_cases(self):
        for query, blocked_response, reference_response \
                in zip(self.df["query"], self.df["response_blocked"], self.df["response_reference"]):
            self.test_cases.append(LLMTestCase(
                input=query,
                actual_output=blocked_response,
                expected_output=reference_response
            ))

    def set_create_metrics(self):
        correctness_metric = GEval(
            model=self.model,
            name="Correctness",
            evaluation_steps=[
                "Check whether the facts in 'actual output' contradicts any facts in 'expected output'",
                "You should also heavily penalize omission of detail and the addition of new claims",
            ],
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
            threshold=0.0
        )
        fluency_metric = GEval(
            model=self.model,
            name="Fluency",
            criteria="Measure how smoothly the text reads, focusing on grammar and syntax",
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=0.0
        )
        relevance_metric = AnswerRelevancyMetric(
            model=self.model,
            include_reason=True,
            threshold=0.0
        )
        self.metrics = [correctness_metric, fluency_metric, relevance_metric]

    def score(self):
        # Get the results
        deepeval_results = evaluate(test_cases=self.test_cases,
                                    metrics=self.metrics,
                                    display_config=self.display_config)
        self.results = rewrite_deepeval_results(deepeval_results=deepeval_results)
        self.df_results_detailed = pd.DataFrame(self.results).sort_values("name")
        self.df_results_detailed["id"] = self.df["id"]

        # Create the df_results (less detailed)
        self.df_results = self.df_results_detailed[["id", "correctness", "fluency", "relevance", "correctness_reason",
                                                    "fluency_reason", "relevance_reason"]]

        # Calculate averages
        self.correctness = self.df_results["correctness"].mean()
        self.fluency = self.df_results["fluency"].mean()
        self.relevance = self.df_results["relevance"].mean()

    def set_non_verbose_display_config(self):
        self.display_config = DisplayConfig(
            print_results=False
        )


def rewrite_deepeval_results(deepeval_results: EvaluationResult) -> list[dict[str, Any]]:
    input_results = deepeval_results.model_dump()["test_results"]
    output_results = []

    for result in input_results:
        base_dict = {
            "name": result["name"],
            "query": result["input"],
            "response_blocked": result["actual_output"],
            "response_reference": result["expected_output"]
        }
        for metric_dict in result["metrics_data"]:
            name = metric_dict["name"].replace("[GEval]", "").strip().replace(" ", "_").lower()
            name = "relevance" if name == "answer_relevancy" else name
            base_dict.update({
                name: metric_dict["score"],
                f"{name}_reason": metric_dict["reason"],
                f"{name}_evaluation_model": metric_dict["evaluation_model"],
                f"{name}_evaluation_cost": metric_dict["evaluation_cost"],
                f"{name}_verbose_logs": metric_dict["verbose_logs"],
            })
        output_results.append(base_dict)
    return output_results


@click.command("Touché Evaluation - Ad Blocking (LLM-as-a-Judge)")
@click.argument('dataset', default='ads-in-rag-task-3-blocking-spot-check-20260424-training', type=str)
@click.option('--truth_file', type=str, help='Path to a local truth_file. If not set, the truths from TIRA will be used')
@click.option('--run_file', type=str, help='Path to a local run file.')
@click.option('--run_id', type=str, help='ID used to identify the run.')
def main(dataset: str,
        truth_file: str = None,
        run_file: str = None,
        run_id: str = None):
    evaluator = BlockingEvaluatorLLM(dataset=dataset,
                                   truth_file=truth_file,
                                   run_file=run_file,
                                   run_id=run_id)
    evaluator.evaluate()


if __name__ == "__main__":
    main()
