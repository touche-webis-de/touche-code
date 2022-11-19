Query Submission Baselines
==========================
Simple query expansion for "Image Retrieval for Arguments".

```
wget https://touche.webis.de/clef23/touche23-data/topics-task3.xml -O topics.xml
docker run --volume $PWD:/data webis/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0 --inputDataset /data --outputDataset /data --proExpansion "good" --conExpansion "anti"
cat query-submission-form-task3.tsv
```


TIRA
----
`python3 /query-submission-baselines.py --inputDataset $inputDataset --outputDataset $outputDir --proExpansion "good" --proExpansion "anti"`


Development
-----------
```
docker build -t webis/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0 .
docker push webis/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0
```

