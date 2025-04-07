# miniLM Baseline for Touché'25 Advertisement Detection

This directory contains a finetuned miniLM model for next sentence predictions to classify if a generated RAG response contains advertisements. This baseline takes the RAG response and the query as input, splits the response into sentence pairs and predicts for each pair whether the second sentence contains an advertisement or not.

## Development

<!--This directory is [configured as DevContainer](https://code.visualstudio.com/docs/devcontainers/containers), i.e., you can open this directory with VS Code or some other DevContainer compatible IDE to work directly in the Docker container with all dependencies installed.-->

To make predictions on a dataset, run:

```
./predict.py --dataset native-ads-2024-validation --output predictions.jsonl
```

The `--dataset` either must point to a local directory or must be the ID of a dataset in TIRA ([tira.io/datasets?query=advertisement](https://archive.tira.io/datasets?query=advertisement) shows an overview of available datasets).

To evaluate your submission locally, you can run the official evaluator locally via (install the tira client via `pip3 install tira`):

```
tira-cli evaluate --directory . --dataset native-ads-2024-validation
```

## Submit to TIRA

To submit this baseline to TIRA, please run (more detailed information are available in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission)):

```
tira-cli code-submission --path . --task advertisement-in-retrieval-augmented-generation-2025 --command '/predict.py
```
