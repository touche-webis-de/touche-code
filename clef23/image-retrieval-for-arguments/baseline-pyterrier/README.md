# PyTerrier Baseline for Task 2 on "Evidence Retrieval for Causal Questions"

Build the baseline via:

```
docker build -t webis/tira-touche23-task-3-pyterrier-baseline:0.0.1 .
```

Start a Jupyter Notebook in this Docker image:

```
docker run --rm -ti \
    -p 8888:8888 \
    -v ${PWD}:/workspace \
    webis/tira-touche23-task-3-pyterrier-baseline:0.0.1 \
    jupyter-lab --allow-root --ip 0.0.0.0
```


```
docker tag webis/tira-touche23-task-3-pyterrier-baseline:0.0.1 registry.webis.de/code-research/tira/tira-user-<YOUR-TEAM-NAME>/pyterrier-baseline:0.0.1
```

```
docker push registry.webis.de/code-research/tira/tira-user-<YOUR-TEAM-NAME>/pyterrier-baseline:0.0.1
```

```
/workspace/run-pyterrier-notebook.py --notebook /workspace/full-rank-pipeline.ipynb --input $inputDataset --output $outputDir

/workspace/run-pyterrier-notebook.py --notebook /workspace/re-rank-pipeline.ipynb --input $inputDataset --output $outputDir
```


```
docker push webis/tira-touche23-task-3-pyterrier-baseline:0.0.1
```

