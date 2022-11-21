Query Submission Evaluator
==========================
Evaluator (currently only validator) for "Image Retrieval for Arguments".

Example usage:
```
# get topics file
wget https://touche.webis.de/clef23/touche23-data/topics-task3.xml -O topics.xml
# run baseline
python3 ../query-submission-baselines/query-submission-baselines.py --inputDataset . --outputDataset run --proExpansion "good" --conExpansion "anti"
# validate baseline run
python3 query-submission-evaluator.py --inputDataset . --inputRun run --outputDataset .
# show validation result
cat evaluation.prototext
```

Development
-----------
```
docker build -t webis/touche-image-retrieval-for-arguments-query-submission-evaluator:0.1.0 .
docker push webis/touche-image-retrieval-for-arguments-query-submission-evaluator:0.1.0
```

In TIRA:
```
python3 /query-submission-evaluator.py --inputDataset $inputDataset --inputRun $inputRun --outputDataset $outputDir
```

