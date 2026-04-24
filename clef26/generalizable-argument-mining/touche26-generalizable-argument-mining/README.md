---
configs:
- config_name: inputs
  data_files:
  - split: test
    path: ["inputs.jsonl"]
- config_name: truths
  data_files:
  - split: test
    path: ["truths.jsonl"]

tira_configs:
  resolve_inputs_to: "."
  resolve_truths_to: "."
  baseline:
    link: https://github.com/touche-webis-de/touche-code/tree/main/clef26/generalizable-argument-mining/naive-baseline
    command: /predict.py --dataset $inputDataset --predict Argument
    format:
      name: ["*.jsonl"]
      config:
        id_field: id
        value_field: label
        format_configuration:
          id_field: id
          value_field: label
        truth_format_configuration:
          id_field: id
          value_field: label
        re_map: {"Argument": 1, "No-Argument": 0}
  input_format:
    name: "*.jsonl"
  truth_format:
    name: "*.jsonl"
    config:
      id_field: id
      value_field: label
  evaluator:
    measures: ["accuracy", "recall", "precision", "f1"]
---

# GAIC-2026 Test Dataset

See the [corresponding repository](https://github.com/TomatenMarc/GAIC-2026/tree/main) for more details.

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
tira-cli dataset-submission --dry-run --path touche26-generalizable-argument-mining --task generalizable-argument-mining --split test
```

This will check that the system-inputs and the truths are valid, it will run the specified baseline on it, will check that the outputs of the basline are valid and will run the evaluation on the baseline to ensure that everything works. All of this is configured in the README.md in the Hugging Face datasets format.

If everything worked, the output should look like:

<img width="1358" height="184" alt="Screenshot from 2026-01-08 17-32-46" src="https://github.com/user-attachments/assets/976648c0-a6e0-410a-bfb1-c949ea2575c5" />


## Step 3: Upload the dataset

Repeat the command from above but remove the `--dry-run` flag.

