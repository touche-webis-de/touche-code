# Evaluator for Debating Systems for Retrieval-Augmented Debating 2025 Sub-Task 1

Evaluates a `simulation.jsonl`.

## Development

The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-evaluator-sub-task-1) when a tag matching `rad25-evaluator-sub-task-1-v*` is pushed.

```{bash}
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "rad25-evaluator-sub-task-1-v$version"
git push origin "rad25-evaluator-sub-task-1-v$version"
```

## TIRA

```{bash}
/app/evaluate.sh --run-directory ${inputRun} --ground-truth-directory ${inputDataset} --output-directory ${outputDir}
```
