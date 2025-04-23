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
tira-cli evaluate --predictions . --dataset ads-in-rag-task-1-generation-spot-check-20250423_1-training
```

## Submit to TIRA

To submit this baseline to TIRA, please run (more details are available in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission)):

```
tira-cli code-submission --path . --task advertisement-in-retrieval-augmented-generation-2025 --dataset ads-in-rag-task-1-generation-spot-check-20250423_1-training --command '/generate.py'
```
