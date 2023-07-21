# Random Baseline TIRA Image for Task 2 @  CLEF 2024 Lab
Random baseline for the task on Human Value Detection.

## Requirements

Model execution requires the packages
- `jupyterlab`,
- `runnb`
- `pandas`, and
- `tira>=0.0.32`
in order to use the `tira-run-notebook`command locally.

## Usage

Local example usage for subtask 1:
```bash
# get arguments file
wget https://zenodo.org/record/T.B.A./files/sentences-training.tsv -O senteces.tsv
# run baseline
tira-run-notebook --input . --output . --notebook random_baseline_notebook.ipynb
# show baseline run
head predictions.tsv
```
In order to run subtask 2 you need to change in the
[notebook](random_baseline_notebook.ipynb)
the second code block to
```python
active_subtask = 2
```
and run again.

### Running on TIRA

For better reproducibility, the models for both subtasks are uploaded as Docker images to
[TIRA](https://www.tira.io/).
```bash
docker build -t registry.webis.de/code-research/tira/TIRA_USER/tira-touche24-task-2-subtask-1-random-baseline:1.0.0 .
docker push registry.webis.de/code-research/tira/TIRA_USER/tira-touche24-task-2-subtask-1-random-baseline:1.0.0
```
To build the image for the second subtask you need to modify the
[notebook](random_baseline_notebook.ipynb)
as described in
[Usage](#usage)
and build the image again with an appropriately different tag.

Both images have the identical run command on TIRA:
```bash
tira-run-notebook --input $inputDataset --output $outputDir --notebook random_baseline_notebook.ipynb
```

## Adapting for complex models

### Including model files

Files within the
[models-folder](models)
can be included by uncommenting the respective line in the
[Dockerfile](Dockerfile).

If your model files are stored on the
[Hugging Face Hub](https://huggingface.co/models)
we provided a simple
[download script](models/download_model_files.py)
which can also be used in Github actions for automated image build and deploy.
```bash
python3 models/download_model_files.py -f models/model_downloads.jsonl
```
If your model repository is private you can pass a Hugging Face Hub access token with the option `-t`.

### Additional TIRA functions

When adapting the jupyter notebook, you don't have to keep the exact syntax for the `predict` function:
```python
def predict(input_list: List) -> List:
```
It is only required if you want to run your model as an inference server.

For more information see the
[TIRA client notes](https://github.com/tira-io/tira/tree/main/python-client#running-jupyter-notebooks-with-tira).

## TODOs

- add/update links