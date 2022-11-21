Query Submission Evaluator
==========================
Evaluator (currently only validator) for "Image Retrieval for Arguments".

```
wget https://touche.webis.de/clef23/touche23-data/topics-task3.xml -O topics.xml
docker run --volume $PWD:/data registry.webis.de/code-research/tira/tira-user-minsc/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0 --inputDataset /data --outputDataset /data/run --proExpansion "good" --conExpansion "anti"
docker run --volume $PWD:/data webis/touche-image-retrieval-for-arguments-query-submission-evaluator:0.1.0 --inputDataset /data --inputRun /data/run --outputDataset /data
cat evaluation.prototext
```


TIRA
----
```
python3 /query-submission-evaluator.py --inputDataset $inputDataset --inputRun $inputRun --outputDataset $outputDir
```


Development
-----------
```
docker build -t webis/touche-image-retrieval-for-arguments-query-submission-evaluator:0.1.0 .
docker push webis/touche-image-retrieval-for-arguments-query-submission-evaluator:0.1.0
```

