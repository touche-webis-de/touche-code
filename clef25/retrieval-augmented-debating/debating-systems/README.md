# Baseline Debating Systems for Retrieval-Augmented Debating 2025

We highly recommend that you use one of our systems as a starting point to develop your own system. They are all build on top of our [base image](base/) to ensure they can be used both within and outside of our submission system TIRA. This also allows you to run your system in [GenIRSim](https://github.com/webis-de/GenIRSim) using the [configuration](base/touche25-rad-tira.json) that we use in TIRA.

Systems:

- [Basic Elastic (Python)](basic-elastic-py/)
- [Basic Elastic (JavaScript)](basic-elastic-js/)

Copy one of the directories that is closest to what you have in mind (e.g., `basic-elastic-py`) to your repository and start from there.

Test:

```{bash}
# Change to your image (e.g., 'myimage' if you build it using 'docker build -t myimage .')
IMAGE=ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-basic-elastic-py:latest

# Run your system in GenIRSim (topics and users as defined in toy-parameter-file.tsv)
docker run --rm -it \
  --volume $PWD:/data \
  --entrypoint /genirsim/run.sh \
  $IMAGE \
  --parameter-file=/data/toy-parameter-file.tsv --output-file=/data/simulation.jsonl

# Output: simulation.jsonl
```
