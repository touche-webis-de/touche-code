# Baseline for Touché'25 Advertisement Generation

This directory contains a simple implementation for generating RAG responses with and without advertisements. This baseline takes as input a query, a list of candidate segments to generate the response, and a list of items to advertise. It returns the segment with the highest relevance score; for responses that should include an advertisement, a simple dummy sentence is appended, containing the item and the qualities that should be promoted.

## Development

<!--This directory is [configured as DevContainer](https://code.visualstudio.com/docs/devcontainers/containers), i.e., you can open this directory with VS Code or some other DevContainer compatible IDE to work directly in the Docker container with all dependencies installed.-->

To generate responses from a dataset, run:

```
./generate.py --dataset ads-in-rag-task-1-generation-spot-check-20250423_1-training --output generations.jsonl
```

The `--dataset` either must point to a local directory or must be the ID of a dataset in TIRA ([tira.io/datasets?query=ads-in-rag-generation](https://archive.tira.io/datasets?query=ads-in-rag-generation) shows an overview of available datasets).

The final evaluation will require access to systems developed during the ad detection tasks (and potentially human judgments). Still, we have a preliminary evaluation that you can use to get a gist on what your system produced and to verify that your generated responses are in the correct format, therefore, you can run the preliminary evaluator locally via (install the tira client via `pip3 install tira`):

```
tira-cli evaluate --predictions generations.jsonl --dataset ads-in-rag-task-1-generation-spot-check-20250423_1-training
```

### Use MiniLM-Baseline to classify your generations
The `tira-cli evaluate`-command confirms that the output format of your generated responses is valid. 
To test if the baseline model is able to detect your advertisements, you can use the [`predict_local.py`](../subtask-2-classification/minilm-baseline/predict_local.py)-script.
*Note: You need to install the respective [requirements](../subtask-2-classification/minilm-baseline/requirements.txt).*
```
../subtask-2-classification/minilm-baseline/predict_local.py
```
Unless specified otherwise, the output is written to `predictions.jsonl`.

## Submit to TIRA
To submit this baseline to TIRA, follow the instructions in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission).
On a high level, you need to perform these steps:

1. Join the task https://www.tira.io/task-overview/advertisement-in-retrieval-augmented-generation-2025
2. Click "Submit" on the task page
3. Choose "Code Submission" or "Run Uploads" and click "New Submission" or "New Approach"
4. Follow the steps shown in the Web UI (Download the TIRA client, authenticate, make the submission)
5. For code submissions: Run the submission using the Web UI

### Code submission
To submit this baseline to TIRA, please run:
```
tira-cli code-submission --path . --task advertisement-in-retrieval-augmented-generation-2025 --dataset ads-in-rag-task-1-generation-spot-check-20250423_1-training --command '/generate.py'
```

#### Running a submission on TIRA
After executing the command above, you will be shown the name of your code submission. Under "Code Submissions" in the Web UI, 
you can select the submission based on the name (and potentially rename it using the "Edit" button). 

Now that your submission is available on TIRA, you can run it on different datasets by using the dropdown menus in the Web UI (see also the [documentation](https://docs.tira.io/participants/participate.html#execute-your-submission)).

### Run submission
To submit the output of this baseline (e.g. `generations.jsonl`), please run:
```
tira-cli upload --dataset ads-in-rag-task-1-generation-spot-check-20250423_1-training --directory ./generations.jsonl --system YOUR_APPROACH
```

### Test Dataset
The name of the test set on TIRA is `ads-in-rag-task-1-generation-test` and its identifier is `ads-in-rag-task-1-generation-test-20250506-test`.

#### Code submission
If you have submitted your code for the spot-check dataset as illustrated under "[Code submission](#code-submission)", you can run it on TIRA as explained under "[Running a submission on TIRA](#running-a-submission-on-tira)".
To do that, select the dataset `ads-in-rag-task-1-generation-test` from the dataset dropdown and run your submitted code. 

#### Run submission
To make a run submission, you can download the test dataset from [Zenodo](https://zenodo.org/records/15347992/files/ads-in-rag-task-1-generation-test.jsonl.gz?download=1) and generate the output.
You can generate output for the local dataset:
```
./generate.py --dataset ./ads-in-rag-task-1-generation-test.jsonl.gz --output generations_test.jsonl
```
And then submit the output (for this baseline):
```
tira-cli upload --dataset ads-in-rag-task-1-generation-test-20250506-test --directory ./generations_test.jsonl --system YOUR_APPROACH
```