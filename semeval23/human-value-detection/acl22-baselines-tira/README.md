# ACL'22-Baselines TIRA Image(s)
Bert-Model and SVM baselines from the ACL'22 publication "[Identifying the Human Values behind Arguments](https://webis.de/publications.html#kiesel_2022b)" for Human Value Detection 2023 @ Touche and SemEval 2023.

Requirement:
- pre-trained model data (in [models/bert](models/bert) and/or [models/svm](models/svm) respectively)

Local example usage:
```bash
# get arguments file
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments.tsv
# run baseline
tira-run-notebook --input . --output . --notebook predict_bert_notebook.ipynb
# or
tira-run-notebook --input . --output . --notebook predict_svm_notebook.ipynb
# show baseline run
head predictions.tsv
```

## Development
```bash
# Bert model
docker build -f Dockerfile_bert_tira -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert-tira:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert-tira:1.0.0
```
or
```bash
# SVM
docker build -f Dockerfile_svm_tira -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm-tira:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm-tira:1.0.0
```

In TIRA:
```bash
# Bert model
tira-run-notebook --input $inputDataset --output $outputDir --notebook /workspace/predict_bert_notebook.ipynb
```
or
```bash
# SVM
tira-run-notebook --input $inputDataset --output $outputDir --notebook /workspace/predict_svm_notebook.ipynb
```

Inference Server:
```bash
# Bert model
mkdir logs/
PORT=8001

docker run --rm -it --init \
  -v "$PWD/logs:/workspace/logs" \
  -p $PORT:$PORT \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert-tira:1.0.0 \
  tira-run-inference-server --notebook /workspace/predict_bert_notebook.ipynb --port $PORT
```
or
```bash
# SVM
mkdir logs/
PORT=8001

docker run --rm -it --init \
  -v "$PWD/logs:/workspace/logs" \
  -p $PORT:$PORT \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm-tira:1.0.0 \
  tira-run-inference-server --notebook /workspace/predict_svm_notebook.ipynb --port $PORT
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
