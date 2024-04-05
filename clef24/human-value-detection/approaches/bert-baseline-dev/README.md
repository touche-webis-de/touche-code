# Bert Baseline for ValueEval'24 (Script)
BERT baseline for the task on Human Value Detection, script version.

The baseline is intended for kickstarting your own approach.
Load your models
etc. at `# SETUP` and then change `predict(text)`. If you keep everything else,
your approach can be directly dockerized, run within Docker on TIRA, and run as
a server that you can call via HTTP or deploy for everyone to use.

## Usage

### Local usage
First download and extract the `valueeval24.zip` from [Zenodo](https://zenodo.org/doi/10.5281/zenodo.10396293).
```bash
# install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export HF_TOKEN=... # Token with write permission from https://huggingface.co/settings/tokens, needed to upload your trained model
export HF_MODEL_NAME=... # Model name under your account. I used "JohannesKiesel/valueeval24-bert-baseline-en" for https://huggingface.co/JohannesKiesel/valueeval24-bert-baseline-en

# train the model
python3 train_bert_baseline.py \
  --training-dataset valueeval24/training-english/ \
  --validation-dataset valueeval24/validation-english/ \
  --model-name "$HF_MODEL_NAME" \
  --model-directory model/

```




## Requirements

Using the models requires the pre-trained model data in
[models/](models)
or train the model
[yourself](#manually-train).

In addition to the packages listed in
[requirements.txt](requirements.txt)
it is necessary to install the packages
- `jupyterlab`,
- `runnb`,
- `pandas` (for the inference server), and
- `tira>=0.0.28`
in order to use the `tira-run-notebook` or `tira-run-inference-server` commands locally.

## Usage

Local example usage:
```bash
# get arguments file
wget https://zenodo.org/record/T.B.A./files/sentences-training.tsv -O senteces.tsv
# run baseline
tira-run-notebook --input . --output . --notebook predict_bert_notebook.ipynb
# show baseline run
head predictions.tsv
```

## Development

### Manually Train
Create docker image
```bash
docker build -f Dockerfile_training -t registry.webis.de/code-research/tira/tira-user-test/tira-touche24-bert-training:1.0.0 .
```
Download training dataset
```
mkdirs dataset/training
wget https://zenodo.org/record/T.B.A./files/sentences-training.tsv -O dataset/training/sentences.tsv
wget https://zenodo.org/record/T.B.A./files/labels-ground_truth-training.tsv -O dataset/training/labels-ground_truth.tsv
```
Train classifier, input files are `$PWD/dataset/training/sentences.tsv` and `$PWD/dataset/training/labels-ground_truth.tsv`
```bash
mkdir models
SUBTASK=1 # or 2 for the second subtask

docker run --rm -it --init \
  --volume "$PWD/dataset/training:/dataset" \
  --volume "$PWD/models:/models" \
  registry.webis.de/code-research/tira/tira-user-test/tira-touche24-bert-training:1.0.0 \
  python3 training.py -s $SUBTASK
# remove pytorch checkpoints
rm -r models/bert_train_subtask_${SUBTASK}/checkpoint-*
```

### Create TIRA Image

Create docker image
```bash
docker build -f Dockerfile_tira -t registry.webis.de/code-research/tira/tira-user-test/tira-touche24-bert-baseline-tira:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-test/tira-touche24-bert-baseline-tira:1.0.0
```

In TIRA:
```bash
export SUBTASK=1 && tira-run-notebook --input $inputDataset --output $outputDir --notebook /workspace/predict_bert_notebook.ipynb
```
or
```bash
export SUBTASK=2 && tira-run-notebook --input $inputDataset --output $outputDir --notebook /workspace/predict_bert_notebook.ipynb
```

Inference Server:
```bash
mkdir logs/
PORT=8001
SUBTASK=1  # or 2 for the second subtask

docker run --rm -it --init \
  -v "$PWD/logs:/workspace/logs" \
  --env SUBTASK=$SUBTASK
  -p $PORT:$PORT \
  registry.webis.de/code-research/tira/tira-user-test/tira-touche24-bert-baseline-tira:1.0.0 \
  tira-run-inference-server --notebook /workspace/predict_bert_notebook.ipynb --port $PORT
```

Exemplary request for a server running on `localhost:8001` are
```bash
# POST (JSON list as payload)
curl -X POST -H "application/json" \
  -d "[\"Sentence 1\", \"Sentence 2\", \"Sentence 3\"]" \
  localhost:8001
```
and
```bash
# GET (JSON object string(s) passed to the 'payload' parameter)
curl "localhost:8001?payload=\"Sentence+1\"&payload=\"Sentence+2\"&payload=\"Sentence+3\""
```
