# Adam Smith for ValueEval'24
ValueEval'23 winner for ValueEval'24

## Usage

```bash
# build
docker build -t valueeval24-adam-smith:1.0.0 .

# run
docker run --rm \
  -v $PWD/../../toy-dataset:/dataset -v $PWD/output:/output \
  valueeval24-adam-smith:1.0.0

# view result
cat output/predictions.tsv
```

### TIRA usage
- Follow the guide on the TIRA submission page to log in with tira-cli.
```
python3 -m venv venv
source venv/bin/activate
pip3 install tira
tira-run --input-dataset valueeval-2024-human-value-detection/valueeval24-2024-04-15-toy-20240614-training --image valueeval24-adam-smith:1.0.0 --command 'bash /adam-smith-wrapper.sh $inputDataset/ $outputDir/'
```

