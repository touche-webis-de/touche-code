1 Baseline
==========
1 baseline for Human Value Detection 2023 @ Touche and SemEval 2023.

```
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments.tsv
docker run --volume $PWD:/data registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-1-baseline:1.0.0 --inputDataset /data --outputDataset /data
head run.tsv
```


TIRA
----
```
python3 /1-baselines.py --inputDataset $inputDataset --outputDataset $outputDir
```


Development
-----------
```
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-1-baseline:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-1-baseline:1.0.0
```

