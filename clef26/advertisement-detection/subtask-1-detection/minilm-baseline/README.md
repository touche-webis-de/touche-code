# miniLM Baseline for Touché'26 Advertisement Detection

This directory contains a finetuned miniLM model for next sentence predictions to classify if a generated RAG response contains advertisements. This baseline takes the RAG response and the query as input, splits the response into sentence pairs and predicts for each pair whether the second sentence contains an advertisement or not.

## Development

If you want to run this baseline locally, please install the dependencies via `pip3 install -r requirements.txt`.

To make predictions on a dataset, run:

```
./predict.py --dataset ads-in-rag-task-1-detection-spot-check-20260422-training --output predictions.jsonl
```

The `--dataset` either must point to a local directory or must be the ID of a dataset in TIRA ([tira.io/datasets?query=ads-in-rag-task-1-detection](https://archive.tira.io/datasets?query=ads-in-rag-task-1-detection) shows an overview of available datasets).

To evaluate your submission locally, you can run the official evaluator locally via (install the tira client via `pip3 install tira`):

```
tira-cli evaluate --predictions . --dataset ads-in-rag-task-1-detection-spot-check-20260422-training
```

## Submit to TIRA
To submit this baseline to TIRA, follow the instructions in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission).
On a high level, you need to perform these steps:

1. Join the task https://www.tira.io/task-overview/advertisement-in-retrieval-augmented-generation-2026
2. Click "Submit" on the task page
3. Choose "Code Submission" and click "New Submission"
4. Follow the steps shown in the Web UI (Download the TIRA client, authenticate, make the submission)
5. Run the submission using the Web UI

### Code submission
To submit this baseline to TIRA, please run:
```
tira-cli code-submission --path . --task advertisement-in-retrieval-augmented-generation-2026 --dataset ads-in-rag-task-1-detection-spot-check-20260422-training --command '/predict.py'
```

#### Running a submission on TIRA
After executing the command above, you will be shown the name of your code submission. Under "Code Submissions" in the Web UI, 
you can select the submission based on the name (and potentially rename it using the "Edit" button). 

Now that your submission is available on TIRA, you can run it on different datasets by using the dropdown menus in the Web UI (see also the [documentation](https://docs.tira.io/participants/participate.html#execute-your-submission)).

### Test dataset
The name of the test set on TIRA is `<to be announced>`.

#### Code submission
If you have submitted your code for the spot-check dataset as illustrated under "[Code submission](#code-submission)", you can run it on TIRA as explained under "[Running a submission on TIRA](#running-a-submission-on-tira)".
To do that, select the dataset `<to be announced>` from the dataset dropdown and run your submitted code.