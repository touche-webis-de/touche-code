# ACL'22-Baselines

Bert-Model and SVM baselines from the ACL'22 publication "[Identifying the Human Values behind Arguments](https://webis.de/publications.html#kiesel_2022b)" for Human Value Detection 2023 @ Touche and SemEval 2023.

## Bert-Model

### Training the classifier
Create docker image
```bash
TAG=1.0.1-nocuda # or 'TAG=1.0.1-cuda11.3' if a GPU is available
CUDA=nocuda # or 'CUDA=cuda11.3' if a GPU is available
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert-training:$TAG --build-arg CUDA=$CUDA -f Dockerfile_bert_training .
```
Download training dataset
```
mkdirs dataset/training
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O dataset/training/arguments.tsv
wget https://zenodo.org/record/6818093/files/labels-training.tsv -O dataset/training/labels-level2.tsv
```
Train classifier, input files are `$PWD/dataset/arguments.tsv` and `$PWD/dataset/labels-level2.tsv`
```bash
mkdir models
TAG=1.0.1-nocuda # or 'TAG=1.0.1-cuda11.3' if a GPU is available
GPUS="" # or 'GPUS="--gpus=all"' to use all GPUs

docker run --rm -it --init $GPUS \
  --volume "$PWD/dataset/training:/dataset" \
  --volume "$PWD/models/bert:/models" \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert-training:$TAG \
  python3 training.py
# remove pytorch checkpoints
rm -r models/bert/bert_train_level2/checkpoint-*
```

### Development
For internal use
```bash
TAG=1.0.1-nocuda # or 'TAG=1.0.1-cuda11.3' if a GPU is available
CUDA=nocuda # or 'CUDA=cuda11.3' if a GPU is available
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert:$TAG --build-arg CUDA=$CUDA -f Dockerfile_bert_predicting .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-bert:$TAG
```
In TIRA:
```bash
python3 /app/predict.py --inputDataset $inputDataset --outputDir $outputDir
```

## SVM

### Training the classifier
Create docker image
```bash
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm-training:1.0.2 -f Dockerfile_svm_training .
```
Download training dataset
```
mkdirs dataset/training
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O dataset/training/arguments.tsv
wget https://zenodo.org/record/6818093/files/labels-training.tsv -O dataset/training/labels-level2.tsv
```
Train classifier, input files are `$PWD/dataset/arguments.tsv` and `$PWD/dataset/labels-level2.tsv`
```bash
mkdir models

docker run --rm -it --init \
  --volume "$PWD/dataset:/dataset" \
  --volume "$PWD/models/svm:/models" \
  registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm-training:1.0.2 \
  python training.py
```

### Development
For internal use
```bash
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm:1.0.2 -f Dockerfile_svm_predicting .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-svm:1.0.2
```
In TIRA:
```bash
python3 /app/predict.py --inputDataset $inputDataset --outputDir $outputDir
```
