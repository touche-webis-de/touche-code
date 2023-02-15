# Adam-Smith

Files for replicating the best performing system
[Adam-Smith](https://github.com/danielschroter/human_value_detector)
of SemEval2023 Task 4 - ValueEval: Identification of Human Values behind Arguments

## Download Models

The trained models can be downloaded under the following link:
[https://drive.google.com/drive/folders/1bN7N9OwT8r35elQZlTEnBpnNHpoBl0Pz?usp=share_link](https://drive.google.com/drive/folders/1bN7N9OwT8r35elQZlTEnBpnNHpoBl0Pz?usp=share_link)

Place them in the
[checkpoints](checkpoints)
directory. 

## Development (NOT YET WORKING)
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

## Remark towards Code Adaptation

The base source code is taken from the `predict.ipynb` file from
[https://github.com/danielschroter/human_value_detector](https://github.com/danielschroter/human_value_detector).

The parts of the code taken directly from the notebook are marked with `START` and `END` comments.
All changes made to these lines are noted directly above each affected expression.
