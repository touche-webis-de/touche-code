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

To submit to TIRA via Docker submission, log in (see instructions when you go to our [TIRA task page](https://www.tira.io/submit/retrieval-augmented-debating-2025), click "SUBMIT", and then on "DOCKER SUBMISSIONS" and "NEW SUBMISSION").

The adapted command to submit for our base systems is:
```{bash}
IMAGE=ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-basic-elastic-py:latest

tira-run \
  --input-dataset retrieval-augmented-debating-2025/rad25-2025-01-16-toy-20250116-training \
  --image $IMAGE \
  --command '/genirsim/run.sh --configuration-file=$inputDataset/*.json --parameter-file=$inputDataset/*.tsv --output-file=$outputDir/simulations.jsonl' \
  --allow-network true \
  --push true
```

For "CODE SUBMISSION" via continuous integration, see the [workflow file for the Python base image](../../../.github/workflows/rad25-basic-elastic-py-tira-upload.yml) and adapt it to your case.

