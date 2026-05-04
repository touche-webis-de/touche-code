---
configs:
- config_name: inputs
  data_files:
  - split: test
    path: ["ads-in-rag-task-2-span-prediction-test.jsonl"]
- config_name: truths
  data_files:
  - split: test
    path: ["ads-in-rag-task-2-span-prediction-test-labels.jsonl"]

tira_configs:
  resolve_inputs_to: "."
  resolve_truths_to: "."
  baseline:
    link: https://github.com/touche-webis-de/touche-code/tree/main/clef26/advertisement-detection/subtask-2-span-prediction
    command: /predict.py
    format:
      name: ["*.jsonl"]
      config:
        id_field: id
        value_field: spans
  input_format:
    name: "*.jsonl"
  truth_format:
    name: "*.jsonl"
    config:
      id_field: id
      value_field: spans
  evaluator:
    image: ghcr.io/touche-webis-de/evaluator-dummy:clef26
    command: python3 /evaluator.py -p ${inputRun} -t ${inputDataset} -o ${outputDir}
---

# Uploading the Dataset to TIRA


## Step 1: Ensure your TIRA Client works

We use [TIRA](https://archive.tira.io) as backend.

Install the tira client via:

```
pip3 install tira
```

Next, check that your TIRA client is correctly installed and that you are authenticated:

```
tira-cli verify-installation
```

If everything is as expected, the output should look like:

```
✓ You are authenticated against www.tira.io.
✓ TIRA home is writable.
✓ Docker/Podman is installed.
✓ The tirex-tracker works and will track experimental metadata.

Result:
✓ Your TIRA installation is valid.
```

## Step 2: Check that the Dataset is Valid and that the baseline and evaluator work

from the parent directory of this README, verify the dataset via:

```
tira-cli dataset-submission --dry-run --path task-2-span-prediction --task advertisement-in-retrieval-augmented-generation-2026 --split test
```

This will check that the system-inputs and the truths are valid, it will run the specified baseline on it, will check that the outputs of the basline are valid and will run the evaluation on the baseline to ensure that everything works. All of this is configured in the README.md in the Hugging Face datasets format.

## Step 3: Upload the dataset

Repeat the command from above but remove the `--dry-run` flag.
