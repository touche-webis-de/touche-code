# Adam-Smith Server

```bash
TAG=1.0.0-cpu # or 'TAG=1.0.0-cuda11.3' if a GPU is available
CUDA=nocuda # or 'CUDA=cuda11.3' if a GPU is available
docker build -t webis-de/valueeval23-adam-smith-server:$TAG -f Dockerfile .
```

To start the server locally on port `8080` (use `PORT_E` to customize externally used port) run:
```bash
TAG=1.0.0-cpu # or 'TAG=1.0.0-cuda11.3' if a GPU is available
GPUS="" # or 'GPUS="--gpus=all"' to use all GPUs
PORT_E=8080
PORT_I=8001

docker run --rm -it --init $GPUS \
  --volume "$PWD/checkpoints/human_value_trained_models:/app/checkpoints/human_value_trained_models" \
  --volume "$PWD/logs:/app/logs" \
  -p $PORT_E:$PORT_I \
  webis-de/valueeval23-adam-smith-server:$TAG --internal_port=$PORT_I --threshold=0.26
```

The required model files can be downloaded under the following link:
[https://zenodo.org/record/7656534](https://zenodo.org/record/7656534)

Place the downloaded zip-Archive in the
[checkpoints](checkpoints)
directory and un-zip the archive (should result in the folder
[checkpoints/human_value_trained_models](checkpoints/human_value_trained_models)
with 24 files inside).


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
with the respectively prefixed `.pkl` and `.ckpt` files present in the mounted folder and using the noted threshold in
the above mentioned `docker run`.