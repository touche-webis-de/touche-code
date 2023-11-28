# Random Baseline for ValueEval'24 (Script)
Random baseline for the task on Human Value Detection, script version.

The baseline is intended for kickstarting your own approach. Load your models
etc. at `# SETUP` and then change `predict(text)`. If you keep everything else,
your approach can be directly dockerized, run within Docker on TIRA, and run as
a server that you can call via HTTP or deploy for everyone to use.

## Usage

### Local usage
```bash
# install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run
python3 random_baseline.py ../../toy-dataset/ output/

# view result
cat output/predictions.tsv
```

### Docker usage
```bash
# build
docker build -t valueeval24-random-baseline:1.0.0 .

# run
docker run --rm \
  -v $PWD/../../toy-dataset:/dataset -v $PWD/output:/output \
  valueeval24-random-baseline:1.0.0

# view result
cat output/predictions.tsv
```

### Server usage
Start a server that provides the `predict`-function over HTTP:
```bash
# Either for local usage (after installation):
tira-run-inference-server --script random_baseline.py --port 8787

# Or for docker usage (after building):
docker run --rm -it --publish 8787:8787 --entrypoint tira-run-inference-server \
  valueeval24-random-baseline-notebook:1.0.0 \
  --script random_baseline.py --port 8787
```
Then in another shell:
```bash
curl -X POST -H "application/json" \
  -d "[\"Our nature must be protected\", \"We do not always get what we want\"]" \
  localhost:8787
```

### TIRA usage
- Follow the guide on the TIRA submission page to upload the model
- Use this for the command: `python /random_baseline.py $inputDataset $outputDir`


## Develop your own approach
- See the [random-baseline-notebook](../random-baseline-notebook/) if you prefer to work with notebooks instead of plain Python scripts
- Modify "Setup" and "Prediction"
- At the start of the [Dockerfile](Dockerfile) is an alternative `FROM` instruction to use PyTorch and GPUs (works with TIRA)
- You can integrate our [model_downloader](../model-downloader/) to download models from Hugging Face Hub

