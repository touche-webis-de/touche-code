# Adam-Smith

Files for replicating the best performing system
[Adam-Smith](https://github.com/danielschroter/human_value_detector)
of SemEval2023 Task 4 - ValueEval: Identification of Human Values behind Arguments

## Download Models

The trained models can be downloaded under the following link:
[https://zenodo.org/record/7656534](https://zenodo.org/record/7656534)

Place the downloaded zip-Archive in the
[checkpoints](checkpoints)
directory.

## Development
<b>Crated image requires >100 GB space!</b>

For internal use
```bash
TAG=1.0.0-nocuda # or 'TAG=1.0.0-cuda11.3' if a GPU is available
CUDA=nocuda # or 'CUDA=cuda11.3' if a GPU is available
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith:$TAG --build-arg CUDA=$CUDA -f Dockerfile .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith:$TAG
```
In TIRA:
```bash
python3 /app/predict.py --inputDataset $inputDataset --outputDir $outputDir
```

## Mounting-Image (NOT YET READY)
As the model data takes a fair amount of space the following describes the 

Unzip the
[downloaded](#download-models)
zip-Archive inside the
[checkpoints](checkpoints)
directory (which should generate a folder `human_value_trained_models`) and build the Image from the home directory with:
```bash
TAG=1.0.0-nocuda # or 'TAG=1.0.0-cuda11.3' if a GPU is available
CUDA=nocuda # or 'CUDA=cuda11.3' if a GPU is available
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith-mount:$TAG --build-arg CUDA=$CUDA -f Dockerfile-mount .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith-mount:$TAG
```
To run the Image use:
```bash
TAG=1.0.0-nocuda # or 'TAG=1.0.0-cuda11.3' if a GPU is available
GPUS="" # or 'GPUS="--gpus=all"' to use all GPUs
inputDataset=/app/inputDataset
outputDir=/app/outputDir

docker run --rm -it --init $GPUS \
  --volume "$PWD/inputDataset:$inputDataset" \
  --volume "$PWD/outputDir:$outputDir" \
  --volume "$PWD/checkpoints/human_value_trained_models:/app/checkpoints/human_value_trained_models" \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-adam-smith-mount:$TAG \
  python3 /app/predict.py --inputDataset $inputDataset --outputDir $outputDir
```

## Test-Image (FOR TESTING ONLY)
Unzip the
[downloaded](#download-models)
zip-Archive inside the
[checkpoints](checkpoints)
directory (which should generate a folder `human_value_trained_models`) and build the Image from the home directory with:
```bash
docker build -t adam-smith-test:1.0.0 -f Dockerfile-test .
```
Run with:
```bash
docker run --rm -it --init \
  --volume "$PWD/checkpoints/human_value_trained_models:/app/checkpoints/human_value_trained_models" \
  adam-smith-test:1.0.0 \
  python3 /app/test.py /app/checkpoints/human_value_trained_models
```

## Remark towards Code Adaptation

The base source code is taken from the `predict.ipynb` file as well as the `data_modules`, `models`, and `toolbox` folders from
[https://github.com/danielschroter/human_value_detector](https://github.com/danielschroter/human_value_detector).

The parts of the code taken directly from the notebook are marked with `START` and `END` comments.
All changes made to lines from the repository are noted directly above each affected expression.
