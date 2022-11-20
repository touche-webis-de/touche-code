Query Submission Baselines
==========================
Simple query expansion for "Image Retrieval for Arguments".

```
wget https://touche.webis.de/clef23/touche23-data/topics-task3.xml -O topics.xml
docker run --volume $PWD:/data registry.webis.de/code-research/tira/tira-user-minsc/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0 --inputDataset /data --outputDataset /data --proExpansion "good" --conExpansion "anti"
cat query-submission-form-task3.tsv
```


TIRA
----
`python3 /query-submission-baselines.py --inputDataset $inputDataset --outputDataset $outputDir --proExpansion "good" --conExpansion "anti"`

> juvenile-pigeon      "good" "anti"
> national-sprite      "fact-checked" "debunked"
> absolute-gulch       "proof" "truth"
> stale-transfer       "illustration" "illustration against"
> trite-application    "diagram" "real numbers"
> sour-buck            "meme" "anti-meme"
> synchronic-semaphore "stats" "real statistics"
> complete-bar         "quote" "bashing quote"
> aged-base            "supporters" "protests"
> complete-cardinality "evidence" "fake"
> nullary-factory      "" ""


Development
-----------
```
docker build -t registry.webis.de/code-research/tira/tira-user-minsc/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-minsc/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0
```


Run All
-------
```
wget https://touche.webis.de/clef23/touche23-data/topics-task3.xml -O topics.xml
rm -rf runs
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/good-anti --proExpansion "good" --conExpansion "anti"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/fact --proExpansion "fact-checked" --conExpansion "debunked"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/proof --proExpansion "proof" --conExpansion "truth"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/illustration --proExpansion "illustration" --conExpansion "illustration against"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/diagram --proExpansion "diagram" --conExpansion "real numbers"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/meme --proExpansion "meme" --conExpansion "anti-meme"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/stats --proExpansion "stats" --conExpansion "real statistics"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/quote --proExpansion "quote" --conExpansion "bashing quote"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/supporters --proExpansion "supporters" --conExpansion "protests"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/supporters --proExpansion "evidence" --conExpansion "fake"
python3 query-submission-baselines.py --inputDataset . --outputDataset runs/supporters --proExpansion "" --conExpansion ""

cat runs/*/*.tsv \
  | grep -v "^number" \
  | awk -F '\t' '{
      printf "%s\tPRO\t%s\n", $1, $3;
      printf "%s\tCON\t%s\n", $1, $4
    }' \
  | sort -g \
  > queries.tsv
rm -rf runs
```

