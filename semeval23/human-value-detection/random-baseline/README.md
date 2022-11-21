Random Baseline
===============
Random baseline for Human Value Detection 2023 @ Touche and SemEval 2023.

Example usage:
```
# get arguments file
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments.tsv
# run baseline
python3 random-baseline.py --inputDataset . --outputDataset .
# show baseline run
head run.tsv
```


Development
-----------
```
docker build -t registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-random-baseline:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-aristotle/touche-human-value-detection-random-baseline:1.0.0
```

In TIRA:
```
python3 /random-baseline.py --inputDataset $inputDataset --outputDataset $outputDir
```

