# PyTerrier Starter and Baseline for Task 2 on "Evidence Retrieval for Causal Questions"

This is the [PyTerrier](https://github.com/terrier-org/pyterrier) baseline for [task 2 on Evidence Retrieval for Causal Questions](https://touche.webis.de/clef23/touche23-web/evidence-retrieval-for-causal-questions.html) in [Touché 2023](https://touche.webis.de/clef23/touche23-web/).

There are two baselines, one full rank retrieval baseline (in [full-rank-pipeline.ipynb](full-rank-pipeline.ipynb)) that uses ChatNoir and one re-ranking baseline that re-ranks the results of some first-stage ranker (in [re-rank-pipeline.ipynb](re-rank-pipeline.ipynb)).

This image comes with a script [run-notebook.py](run-notebook.py) that allows you to run a PyTerrier retrieval pipeline implemented in a Jupyter Notebook in TIRA.

## Prerequisities:

You need to [install docker](https://docs.docker.com/get-docker/) on your machine.


## Run a Jupyter Notebook locally for Development

We have published this starter image on DockerHub so that you can directly run a notebook with everything installed with the following command:

```
docker run --rm -ti \
    -p 8888:8888 \
    -v ${PWD}:/workspace \
    webis/tira-touche23-task-2-pyterrier-baseline:0.0.1 \
    jupyter-lab --allow-root --ip 0.0.0.0
```

You can adapt/run the baseline notebooks locally locally with docker and can directly deploy and run it in [TIRA.io](https://www.tira.io/task/touche-2023-task-2).



## Full Rank Starter with ChatNoir

The notebook [full-rank-pipeline.ipynb](full-rank-pipeline.ipynb) implements "full-rank" retrieval with ChatNoir so that the results retrieved by ChatNoir can be easily re-ranked.

You can run it on a small example dataset in your notebook.
To test your pipeline locally, you can make run the script [run-notebook.py](run-notebook.py) as `local-dry-run`, e.g., by:

```
./run-notebook.py \
    --input ${PWD}/sample-input/full-rank \
    --output ${PWD}/sample-output \
    --notebook /workspace/full-rank-pipeline.ipynb \
    --enable-network-in-dry-run True --local-dry-run True
```

### Deploy and Run the Full Rank Starter in TIRA

First, you have to upload the image to TIRA.
TIRA gives you personalized credentials to upload your image:



If you already have docker installed on your machine, you can build the image via:

```
docker build -t webis/tira-touche23-task-2-pyterrier-baseline:0.0.1 .
```



Upload the image to TIRA:

```
docker tag webis/tira-touche23-task-2-pyterrier-baseline:0.0.1 registry.webis.de/code-research/tira/tira-user-<YOUR_TEAM_NAME>/pyterrier-baseline:0.0.1
docker push registry.webis.de/code-research/tira/tira-user-<YOUR_TEAM_NAME>/pyterrier-baseline:0.0.1
```

With the image uploaded, you can add the full-rank baseline with the following command in TIRA:

```
/workspace/run-pyterrier-notebook.py --notebook /workspace/full-rank-pipeline.ipynb --input $inputDataset --output $outputDir
```

With the image uploaded, you can add the re-rank baseline with the following command in TIRA:

```
/workspace/run-pyterrier-notebook.py --notebook /workspace/re-rank-pipeline.ipynb --input $inputDataset --output $outputDir
```



# Additional Resources

- The [PyTerrier tutorial](https://github.com/terrier-org/ecir2021tutorial)
- The [PyTerrier documentation](https://pyterrier.readthedocs.io/en/latest/)
- The [TIRA quickstart](https://touche.webis.de/clef23/touche23-web/evidence-retrieval-for-causal-questions.html#tira-quickstart)


# Publishing this image

We publish this image via the following command:

```
docker push webis/tira-touche23-task-2-pyterrier-baseline:0.0.1
```

