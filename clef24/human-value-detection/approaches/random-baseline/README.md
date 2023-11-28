# Random Baseline for ValueEval'24 (Script)
Random baseline for the task on Human Value Detection, script version.


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
docker run --rm -v $PWD/../../toy-dataset:/dataset -v $PWD/output:/output valueeval24-random-baseline:1.0.0

# view result
cat output/predictions.tsv
```

### TIRA usage
- Follow the guide on the TIRA submission page to upload the model
- Use this for the command: `python /random_baseline.py $inputDataset $outputDir`


## Develop your own approach
- See the [random-baseline-notebook](../random-baseline-notebook/) if you prefer to work with notebooks instead of plain Python scripts
- Modify "Setup" and "Prediction"
- At the start of the [Dockerfile](Dockerfile) is an alternative `FROM` instruction to use PyTorch and GPUs (works with TIRA)
- You can integrate our [model_downloader](../model-downloader/) to download models from Hugging Face Hub

