from abc import ABC, abstractmethod
import json
from pathlib import Path
from tira.rest_api_client import Client

TASK_DIR = Path(__file__).parent
SUBMISSION_DIR = TASK_DIR / "submissions"
EVALUATION_DIR = TASK_DIR / "evaluation"


class Evaluator(ABC):
    def __init__(self,
                 dataset: str,
                 truth_file: str = None,
                 run_file: str = None,
                 run_id: str = None):
        # If a run_id was provided, ensure that only one run_file exists
        if run_id:
            run_dir = SUBMISSION_DIR / dataset / run_id / "output"
            run_files = [x for x in run_dir.glob("*.jsonl")]
            assert len(run_files) == 1, f"The number of files in {run_dir} needs to be 1 but it is {len(run_files)}."
            self.run_file = run_files[0]

        elif run_file:
            self.run_file = run_file
            run_id = Path(run_file).stem.split(".")[0]

        else:
            print("Either a run_file or a run_id needs to be provided")
            exit(1)

        self.tira = Client()

        # Read the run results
        self.df = self.tira.pd.inputs(self.run_file)

        # Try to read the truths from a truth_file or TIRA (Only possible for public datasets)
        if truth_file:
            self.truths = self.tira.pd.inputs(truth_file)
        else:
            try:
                self.truths = self.tira.pd.truths(dataset)
            except:
                print(f"\nFailed to read truths for dataset {dataset}.")
                print("Please provide a local truth_file")
                exit(1)

        # Define the output path (Reduce the dataset to its stem if a path is provided
        if "/" in dataset:
            dataset = dataset.split("/")[-1].split(".")[0]

        self.eval_dir = EVALUATION_DIR / dataset / run_id
        self._create_evaluation_folders()
        self.score_path = self.eval_dir / "scores.json"

        # Create the result attribute
        self.result = None

    def _create_evaluation_folders(self):
        if not self.eval_dir.exists():
            self.eval_dir.mkdir(parents=True)

    @abstractmethod
    def score_run(self):
        """
        Evaluate the inputs in self.df based on the truths in self.truths.
        Create a dictionary from the evaluation results and store it in self.result
        """
        pass

    def evaluate(self):
        self.score_run()
        if self.result is None:
            print("The evaluation result is empty. Please verify the evaluator")
            exit(1)

        with open(self.score_path, "w") as f:
            json.dump(self.result, f)

        print("Evaluation Result:")
        print(self.result)
        print(f"\nSaved result to {self.score_path}")