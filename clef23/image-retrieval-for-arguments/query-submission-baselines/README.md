Query Submission Baselines
==========================
Simple query expansion for "Image Retrieval for Arguments".

Example usage:
```
# get topics file
wget https://touche.webis.de/clef23/touche23-data/topics-task3.xml -O topics.xml
# run baseline
python3 query-submission-baselines.py --inputDataset . --outputDataset . --proExpansion "good" --conExpansion "anti"
# show baseline run
cat query-submission-form-task3.tsv
```

You can use the <a href="https://github.com/touche-webis-de/touche-code/blob/main/clef23/image-retrieval-for-arguments/query-submission-baselines/query-submission-baselines.py">baseline code</a> for writing your own query expansion algorithm. But note that it is also possible to submit run files directly in TIRA, and that this task also allows to submit manually created queries this way.


Development
-----------
Internal usage.

```
docker build -t registry.webis.de/code-research/tira/tira-user-minsc/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0 .
docker push registry.webis.de/code-research/tira/tira-user-minsc/touche-image-retrieval-for-arguments-query-submission-baselines:1.0.0
```

In TIRA:
```
python3 /query-submission-baselines.py --inputDataset $inputDataset --outputDataset $outputDir --proExpansion "good" --conExpansion "anti"
```

| TIRA name            | proExpansion   | conExpansion           |
| -------------------- | -------------- | ---------------------- |
| juvenile-pigeon      | "good"         | "anti"                 |
| national-sprite      | "fact-checked" | "debunked"             |
| absolute-gulch       | "proof"        | "truth"                |
| stale-transfer       | "illustration" | "illustration against" |
| trite-application    | "diagram"      | "real numbers"         |
| sour-buck            | "meme"         | "anti-meme"            |
| synchronic-semaphore | "stats"        | "real statistics"      |
| complete-bar         | "quote"        | "bashing quote"        |
| aged-base            | "supporters"   | "protests"             |
| complete-cardinality | "evidence"     | "fake"                 |
| nullary-factory      | ""             | ""                     |

