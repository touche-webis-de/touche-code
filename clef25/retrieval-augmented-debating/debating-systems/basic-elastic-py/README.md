# Basic Debating System for Retrieval-Augmented Debating 2025 (Python)

Simple system ([one file](main.py)) that just replies with the first counter argument retrieved by our Elasticsearch index.

For all the possible ways to use this image (retrieval server, GenIRSim server, GenIRSim run), see the [Entrypoints](https://github.com/touche-webis-de/touche-code/blob/main/clef25/retrieval-augmented-debating/debating-systems/base/README.md#entrypoints) section of the base image README.

## Quickstart
```
# Start the system; use CTRL-C to stop it after use
docker run --rm -it -p 127.0.0.1:8080:8080 ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-basic-elastic-py:latest

# Request the API in a different terminal
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{
  "messages": [
    {"role":"user","content":"I think that it is always wrong to lie since the ten commandments tell us so."},
    {"role":"assistant","content":"I actually think theres a strong case to be made for the idea that \"There is nothing inherently morally wrong about lying.\" In certain situations, like protecting someones life or preventing harm, lying might be seen as a morally justifiable action."},
    {"role":"user","content":"But \"preventing harm\" is a slippery slope."}
  ]
}'
```

## Submit to TIRA

Run the following command (add `--dry-run` for a test, omit the `--dry-run` argument to upload to TIRA):

```
tira-cli code-submission --path . --task retrieval-augmented-debating-2025 --command '/genirsim/run.sh --configuration-file=$inputDataset/*.json --parameter-file=$inputDataset/*.tsv --output-file=$outputDir/simulations.jsonl' --allow-network --dry-run
```

## Development
The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-basic-elastic-py) when a tag matching `rad25-basic-elastic-py-v*` is pushed.
```
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "rad25-basic-elastic-py-v$version"
git push origin "rad25-basic-elastic-py-v$version"
```

