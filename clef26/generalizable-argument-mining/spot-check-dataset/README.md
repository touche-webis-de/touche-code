---
configs:
- config_name: inputs
  data_files:
  - split: train
    path: ["inputs.jsonl"]
- config_name: truths
  data_files:
  - split: train
    path: ["truths.jsonl"]

tira_configs:
  baseline:
    link: https://github.com/reneuir/lsr-benchmark/tree/main/step-03-retrieval-approaches/pyterrier-naive
    command: /run-pyterrier.py --dataset $inputDataset --retrieval BM25 --output $outputDir
    format:
      name: [".jsonl"]
  input_format:
    name: ".jsonl"
  truth_format:
    name: ".jsonl"
  evaluator:
    measures: ["accuracy", "recall", "precision", "f1"]
---

# This is a tiny spot check dataset for 

TODO: some description.


