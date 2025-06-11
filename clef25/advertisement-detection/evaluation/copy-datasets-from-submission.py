#!/usr/bin/env python3
import shutil
from pathlib import Path
shutil
import json

SRC_DIR = Path("/mnt/ceph/storage/data-in-progress/data-research/web-search/TOUCHE-25/advertisement-in-retrieval-augmented-generation/datasets_from_submissions")
TRUTH_DIR = Path("/mnt/ceph/tira/data/datasets/test-datasets-truth/advertisement-in-retrieval-augmented-generation-2025")
INPUTS_DIR = Path("/mnt/ceph/tira/data/datasets/test-datasets/advertisement-in-retrieval-augmented-generation-2025")

MAPPING = {
    "generations-01": "2025-05-25-06-26-11",
    "generations-02": "2025-05-25-10-56-44",
    "generations-03": "2025-05-25-23-01-41",
    "generations-04": "2025-05-26-09-02-02",
    "generations-05": "2025-06-03-15-15-45",
}

print("copy truth data")
for k, v in MAPPING.items():
    target_file = TRUTH_DIR / f'ads-in-rag-task-2-classification-on-{k}-20250611-test' / f'{v}-labels.jsonl'
    src_file = SRC_DIR / f'{v}-labels.jsonl'
    shutil.copy(src_file, target_file)
print("done.")

print("copy system inputs.")
for k, v in MAPPING.items():
    target_file = INPUTS_DIR / f'ads-in-rag-task-2-classification-on-{k}-20250611-test' / 'inputs.jsonl'
    with open(SRC_DIR / f'{v}.jsonl', 'r') as src_file, open(target_file, "w") as f:
        for l in src_file:
            l = json.loads(l)
            l["meta_topic"] = l["metatopic"]
            del l["metatopic"]
            if not l["response"]:
                l["response"] = ""
            f.write(json.dumps(l) + "\n")

