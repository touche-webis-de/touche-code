Human Value Detection Evaluator
===============================

```
mkdir -p labels arguments run
wget https://zenodo.org/record/6818093/files/labels-training.tsv -O labels/labels-training.tsv
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments/arguments-training.tsv
docker run --volume $PWD/arguments:/arguments --volume $PWD/run:/run registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-random-baseline:1.0.0 --inputDataset /arguments --outputDataset /run
docker run --volume $PWD:/data webis/touche-human-value-detection-evaluator:0.1.0 --inputDataset /data/labels --inputRun /data/run --outputDataset /data
cat evaluation.prototext
```


TIRA
----
```
python3 /evaluator.py --inputDataset $inputDataset --inputRun $inputRun --outputDataset $outputDir
```


Development
-----------
```
docker build -t webis/touche-human-value-detection-evaluator:0.1.0 .
docker push webis/touche-human-value-detection-evaluator:0.1.0
```

