# Baseline for Touché'25 Advertisement Generation

This directory contains a simple implementation for generating RAG responses with and without advertisements. This baseline takes as input a query, a list of candidate segments to generate the response, and a list of items to advertise. It returns the segment with the highest relevance score; for responses that should include an advertisement, a simple dummy sentence is appended, containing the item and the qualities that should be promoted.

## Development

<!--This directory is [configured as DevContainer](https://code.visualstudio.com/docs/devcontainers/containers), i.e., you can open this directory with VS Code or some other DevContainer compatible IDE to work directly in the Docker container with all dependencies installed.-->

To make predictions on a dataset, run:

```
./predict.py --dataset touche-25-ads-in-rag-generation --output predictions.jsonl
```

The `--dataset` either must point to a local directory or must be the ID of a dataset in TIRA ([tira.io/datasets?query=advertisement](https://archive.tira.io/datasets?query=advertisement) shows an overview of available datasets).

To evaluate your submission locally, you can run the official evaluator locally via (install the tira client via `pip3 install tira`):

```
tira-cli evaluate --directory . --dataset touche-25-ads-in-rag-generation-20250325_1-training
```

## Submit to TIRA

To submit this baseline to TIRA, please run (more detailed information are available in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission)):

```
tira-cli code-submission --path . --task advertisement-in-retrieval-augmented-generation-2025 --dataset touche-25-ads-in-rag-generation-20250325_1-training --command '/predict.py'
```
