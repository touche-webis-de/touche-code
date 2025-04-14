# Naive Bayes Baseline for Touché'25 Advertisement Detection

This directory contains a naive bayes implementation for classifying if a generated RAG response contains advertisements. This baseline takes the RAG response as input (i.e., without taking the query into account, a potential idea for improvement could be to take the query into account as well).

## Development

This directory is [configured as DevContainer](https://code.visualstudio.com/docs/devcontainers/containers), i.e., you can open this directory with VS Code or some other DevContainer compatible IDE to work directly in the Docker container with all dependencies installed.

If you want to run it locally, please install the dependencies via `pip3 install -r requirements.txt`.

To make predictions on a dataset, run:

```
./predict.py --dataset native-ads-2024-spot-check --output predictions.jsonl --threshold 0.25
```

The `--dataset` either must point to a local directory or must be the ID of a dataset in TIRA ([tira.io/datasets?query=native-ads](https://archive.tira.io/datasets?query=native-ads) shows an overview of available datasets.

To evaluate your submission locally, you can run the official evaluator locally via (install the tira client via `pip3 install tira`):

```
tira-cli evaluate --directory . --dataset native-ads-2024-spot-check
```

## Submit to TIRA

To submit this baseline to TIRA, please run (more detailed information are available in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission):

```
tira-cli code-submission --path . --task advertisement-in-retrieval-augmented-generation-2025 --dataset native-ads-2024-spot-check-20250414-training --command '/predict.py --threshold 0.25'
```

## Train the Model

To train the naive bayes model, run:

```
./train.py
```
