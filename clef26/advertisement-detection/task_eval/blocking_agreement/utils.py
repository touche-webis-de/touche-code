import json
from pathlib import Path

DIMENSIONS = ["relevance", "correctness", "fluency"]


def load_annotations(directory: Path) -> dict[str, dict[str, dict]]:
    """Return {annotator_name: {item_id: {dimension: value}}}."""
    annotators = {}
    for path in sorted(directory.glob("element_scores_manual_*.jsonl")):
        items = {}
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                item_id = record["id"]
                items[item_id] = {dim: record[dim] for dim in DIMENSIONS if dim in record}
        if items:
            annotators[path.name] = items
    return annotators