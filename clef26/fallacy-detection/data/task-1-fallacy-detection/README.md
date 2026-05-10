---
configs:
- config_name: inputs
  data_files:
  - split: test
    path: ["touchefallacy_2026_test_task.jsonl"]
- config_name: truths
  data_files:
  - split: test
    path: ["touchefallacy_2026_test_task.jsonl"]

tira_configs:
  resolve_inputs_to: "."
  resolve_truths_to: "."
  baseline:
    link: https://github.com/touche-webis-de/touche-code/tree/main/clef26/fallacy-detection/naive-baseline
    command: /predict.py --task fallacy_detection --predict fallacy --output $outputDir/predictions.jsonl
    format:
      name: ["*.jsonl"]
      config:
        id_field: id
        value_field: label
        required_fields: ["task", "id", "label", "tag", "system_description"]
        format_configuration:
          id_field: id
          value_field: label
        truth_format_configuration:
          id_field: id
          value_field: id
  input_format:
    name: "*.jsonl"
  truth_format:
    name: "*.jsonl"
    config:
      id_field: id
      value_field: id
  evaluator:
    image: mam10eks/fallacy-detection:eval-0.0.1
    command: "/evalaute.py --task fallacy_detection --dataset $inputDataset --run $inputRun --output $outputDir"
---

# Task 1 Fallacy Detection

```
tira-cli dataset-submission --dry-run --path task-1-fallacy-detection --task fallacy-detection --split test
```

