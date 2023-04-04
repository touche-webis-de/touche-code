# Random Baseline TIRA Image
Random baseline for Human Value Detection 2023 @ Touche and SemEval 2023.

Local example usage:
```bash
# get arguments file
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments.tsv
# run baseline
tira-run-notebook --input . --output . --notebook random_baseline_notebook.ipynb
# show baseline run
head run.tsv
```

## Development
```bash
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-random-baseline-tira:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-random-baseline-tira:1.0.0
```

In TIRA:
```bash
tira-run-notebook --input $inputDataset --output $outputDir --notebook /workspace/random_baseline_notebook.ipynb
```

Inference Server:
```bash
mkdir logs/
PORT=8001

docker run --rm -it --init \
  -v "$PWD/logs:/workspace/logs" \
  -p $PORT:$PORT \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-random-baseline-tira:1.0.0 \
  tira-run-inference-server --notebook /workspace/random_baseline_notebook.ipynb --port $PORT
```
Exemplary request for a server running on `localhost:8001` are
```bash
# POST (JSON list as payload)
curl -X POST -H "application/json" \
  -d "[\"Argument 1\", \"Argument 2\", \"Argument 3\"]" \
  localhost:8001
```
and
```bash
# GET (JSON object string(s) passed to the 'payload' parameter)
curl "localhost:8001?payload=\"Argument+1\"&payload=\"Argument+2\"&payload=\"Argument+3\""
```
