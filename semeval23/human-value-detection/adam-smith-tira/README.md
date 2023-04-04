# Adam-Smith TIRA Image
Dockerized version of the winning submission to ValueEval'23 by Schroter et al. [[original code](https://github.com/danielschroter/human_value_detector)]

## Usage

The required model files can be downloaded under the following link:
[https://zenodo.org/record/7656534](https://zenodo.org/record/7656534)

Place the downloaded zip-Archive in the
[checkpoints](checkpoints)
directory and un-zip the archive (should result in the folder
[checkpoints/human_value_trained_models](checkpoints/human_value_trained_models)
with 24 files inside).

The server can be customized in regards of the model files present in the mounted
`checkpoints/human_value_trained_models` folder. Some configurations with their associated ensemble threshold
(required as command-line argument for the following `docker run`) are as follows:
- `EN-219-Thres-LoD` (all 12 models)
  - using `HCV-364`, `HCV-366`, `HCV-368`, `HCV-371`, `HCV-372`, `HCV-373`, `HCV-402`, `HCV-403`, `HCV-405`, `HCV-406`, `HCV-408`, `HCV-409`
  - `--threshold=0.26`
- `EN-243-Max-F1` (6 models)
  - using `HCV-402`, `HCV-403`, `HCV-405`, `HCV-406`, `HCV-408`, `HCV-409`
  - `--threshold=0.26`
- `EN-236-Deberta-F1` (3 models)
  - using `HCV-406`, `HCV-408`, `HCV-409`
  - `--threshold=0.27`
- `Single-Deberta-F1` (1 model)
  - using `HCV-409`
  - `--threshold=0.25`

Note: For each model the respectively prefixed `.pkl` and `.ckpt` files need to be present in the
mounted `checkpoints/human_value_trained_models` folder and for building the
[Image](#Development),
the respective `ADD` statements for each `.ckpt` file needs to be added to the
[Dockerfile](Dockerfile)
as due to their size each file requires its own layer
(currently only `HCV-409` is present).
Alternatively, the folder `checkpoints/human_values_trained_models` can be mounted on running the image (does not work on TIRA).

Local example usage:
```bash
# get arguments file
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments.tsv
# run baseline
tira-run-notebook --input . --output . --notebook adam_smith_notebook.ipynb
# show run
head predictions.tsv
```

## Development
```bash
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith-tira:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith-tira:1.0.0
```

In TIRA:
```bash
tira-run-notebook --input $inputDataset --output $outputDir --notebook /workspace/adam_smith_notebook.ipynb
```

Inference Server:
```bash
mkdir logs/
PORT=8001

docker run --rm -it --init \
  -v "$PWD/logs:/workspace/logs" \
  -p $PORT:$PORT \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith-tira:1.0.0 \
  tira-run-inference-server --notebook /workspace/adam_smith_notebook.ipynb --port $PORT
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
