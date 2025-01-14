# Baseline Debating Systems for Retrieval-Augmented Debating 2025


- [Base](base/). Code for the base docker image which already contains the required user simulation logic.


```
docker run --rm -it \
  --volume $PWD:/data \
  --entrypoint /genirsim/run.sh
  ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-basic-elastic-js:latest \
  --parameter-file=/data/toy-parameter-file.tsv --output-file=/data/simulation.jsonl
```
