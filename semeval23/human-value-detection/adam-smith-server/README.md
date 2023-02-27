# Adam-Smith Server

## Build Docker Image

```bash
TAG=1.0.0-cpu # or 'TAG=1.0.0-cuda11.3' if a GPU is available
CUDA=nocuda # or 'CUDA=cuda11.3' if a GPU is available
docker build -t webis-de/valueeval23-adam-smith-server:$TAG -f Dockerfile .
```

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
mounted `checkpoints/human_value_trained_models` folder.

To start the server locally on port `8080` (use `PORT_E` to customize externally used port) run:
```bash
TAG=1.0.0-cpu # or 'TAG=1.0.0-cuda11.3' if a GPU is available
GPUS="" # or 'GPUS="--gpus=all"' to use all GPUs
PORT_E=8080
PORT_I=8001
LOG_FOLDER=$PWD/logs

docker run --rm -it --init $GPUS \
  --volume "$PWD/checkpoints/human_value_trained_models:/app/checkpoints/human_value_trained_models" \
  --volume "$LOG_FOLDER:/app/logs" \
  -p $PORT_E:$PORT_I \
  webis-de/valueeval23-adam-smith-server:$TAG --internal_port=$PORT_I --threshold=0.26
```

## Requests

Exemplary request for a server running on `localhost:8080` (cf. `PORT_E`) are
```bash
# POST (argument-string as payload)
curl -X POST -H "text/plain" \
  -d "affirmative action helps with employment equality. against We should end affirmative action" \
  localhost:8080
```
and
```bash
# GET (argument-string as query parameter 'argument')
curl "localhost:8080?argument=affirmative+action+helps+with+employment+equality.+against+We+should+end+affirmative+action"
```
with both resulting (on successful server response) in a JSON object with the arguments
[classification](https://touche.webis.de/semeval23/touche23-web/index.html#task):
```json
{
  "Self-direction: thought": "0",
  "Self-direction: action": "0",
  "Stimulation": "0",
  "Hedonism": "0",
  "Achievement": "1",
  "Power: dominance": "0",
  "Power: resources": "0",
  "Face": "0",
  "Security: personal": "1",
  "Security: societal": "0",
  "Tradition": "0",
  "Conformity: rules": "0",
  "Conformity: interpersonal": "0",
  "Humility": "0",
  "Benevolence: caring": "0",
  "Benevolence: dependability": "0",
  "Universalism: concern": "1",
  "Universalism: nature": "0",
  "Universalism: tolerance": "0",
  "Universalism: objectivity": "0"
}
```