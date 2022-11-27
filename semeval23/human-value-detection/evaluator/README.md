Human Value Detection Evaluator
===============================
Evaluator for Human Value Detection 2023 @ Touche and SemEval 2023.

Example usage:
```
# get resources
mkdir -p labels arguments run
wget https://zenodo.org/record/6818093/files/labels-training.tsv -O labels/labels-training.tsv
wget https://zenodo.org/record/6818093/files/arguments-training.tsv -O arguments/arguments-training.tsv
# run baseline
python3 ../1-baseline/1-baseline.py --inputDataset arguments --outputDataset run
# evaluate baseline run
python3 evaluator.py --inputDataset labels --inputRun run --outputDataset .
# show evaluation result
cat evaluation.prototext
```


Development
-----------
```
docker build -t webis/touche-human-value-detection-evaluator:0.1.2 .
docker push webis/touche-human-value-detection-evaluator:0.1.2
```

In TIRA:
```
python3 /evaluator.py --inputDataset $inputDataset --inputRun $inputRun --outputDataset $outputDir
```

