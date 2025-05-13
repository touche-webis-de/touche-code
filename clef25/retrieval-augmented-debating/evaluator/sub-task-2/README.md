# Evaluator for Debating Systems for Retrieval-Augmented Debating 2025 Sub-Task 2

Evaluates an `evaluation.jsonl`.

## Development

The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-evaluator-sub-task-2) when a tag matching `rad25-evaluator-sub-task-2-v*` is pushed.

```{bash}
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "rad25-evaluator-sub-task-2-v$version"
git push origin "rad25-evaluator-sub-task-2-v$version"
```

## TIRA

```{bash}
python3 /evaluate.py --run-directory ${inputRun} --input-directory ${inputDataset} --output-directory ${outputDir}
```
