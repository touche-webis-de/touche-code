# Bert Baseline for ValueEval'24 (Script)
BERT baseline for the task on Human Value Detection, script version.

The baseline is intended for kickstarting your own approach.
Load your models
etc. at `# SETUP` and then change `predict(text)`. If you keep everything else,
your approach can be directly dockerized, run within Docker on TIRA, and run as
a server that you can call via HTTP or deploy for everyone to use.

## Training
A trained model is available as "JohannesKiesel/valueeval24-bert-baseline-en"

First download and extract the `valueeval24.zip` from [Zenodo](https://zenodo.org/doi/10.5281/zenodo.10396293).
```bash
# install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export HF_TOKEN=... # Token with write permission from https://huggingface.co/settings/tokens, needed to upload your trained model
export HF_MODEL_NAME=... # Model name under your account. I used "JohannesKiesel/valueeval24-bert-baseline-en" for https://huggingface.co/JohannesKiesel/valueeval24-bert-baseline-en

# train the model
#   specify --model-directory to save the model to disk
#   specify --model-name to upload the model to huggingface
python3 train_bert_baseline.py \
  --training-dataset valueeval24/training-english/ \
  --validation-dataset valueeval24/validation-english/ \
  --model-name "$HF_MODEL_NAME" \
  --model-directory model/
```

## Usage
If you trained your own model, change the `model_path` in `bert_baseline.py`.

### Local usage
```bash
# install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run
python3 bert_baseline.py ../../toy-dataset/ output/

# view result
cat output/predictions.tsv
```

### Docker usage
```bash
# build
docker build -t valueeval24-bert-baseline:1.0.0 .

# run
docker run --rm \
  -v $PWD/../../toy-dataset:/dataset -v $PWD/output:/output \
  valueeval24-bert-baseline:1.0.0

# view result
cat output/predictions.tsv
```

### Server usage
Start a server that provides the `predict`-function over HTTP:
```bash
# Either for local usage (after installation):
tira-run-inference-server --script bert_baseline.py --port 8787

# Or for docker usage (after building):
docker run --rm -it --publish 8787:8787 --entrypoint tira-run-inference-server \
  valueeval24-bert-baseline:1.0.0 \
  --script bert_baseline.py --port 8787
```
Then in another shell:
```bash
curl -X POST -H "application/json" \
  -d "[\"Our nature must be protected\", \"We do not always get what we want\"]" \
  localhost:8787
```

