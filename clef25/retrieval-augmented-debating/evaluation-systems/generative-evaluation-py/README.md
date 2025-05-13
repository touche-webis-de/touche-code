# Generative Evaluation System for Retrieval-Augmented Debating 2025 Sub-Task 2 (Python)

Simple system ([one file](main.py)) that just prompts a generative model.

For all the possible ways to use this image (retrieval server, GenIRSim server, GenIRSim run), see the [Entrypoints](https://github.com/touche-webis-de/touche-code/blob/main/clef25/retrieval-augmented-debating/debating-systems/base/README.md#entrypoints) section of the base image README.

## Quickstart

```{bash}
# Run the system on ../toy-simulation.jsonl to create ../toy-evaluation.jsonl
docker run --rm -it \
  --volume $PWD/../:/data \
  --entrypoint /genirsim/run.sh \
  ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-generative-evaluation-py \
  --evaluate-run-file=/data/toy-simulation.jsonl \
  --output-file=/data/toy-evaluation.jsonl
```

## Submit to TIRA

Run the following command (add `--dry-run` for a test, omit the `--dry-run` argument to upload to TIRA):

```{bash}
tira-cli code-submission --path . --task retrieval-augmented-debating-2025 --command '/genirsim/run.sh --evaluate-run-file=$inputDataset/*.json --output-file=$outputDir/simulations.jsonl' --allow-network --dry-run
```

For submission via continuous integration, see the [workflow file for this image](../../../../.github/workflows/rad25-generative-evaluation-py-tira-upload.yml) and adapt it to your case.

## Development

The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-generative-evaluation-py) when a tag matching `rad25-generative-evaluation-py-v*` is pushed.

```{bash}
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "rad25-generative-evaluation-py-v$version"
git push origin "rad25-generative-evaluation-py-v$version"
```
