# Evaluator for Debating Systems for Retrieval-Augmented Debating 2025

Evaluates a `simulation.jsonl`.


## Development
The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-evaluator) when a tag matching `rad25-evaluator-v*` is pushed.
```
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "rad25-evaluator-v$version"
git push origin "rad25-evaluator-v$version"
```

## TIRA
```
/app/evaluate.sh --run-directory=${inputRun} --ground-truth-directory=${inputDataset} --output-directory=${outputDir}
```

