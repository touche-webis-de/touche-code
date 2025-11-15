import json
from pathlib import Path
import settings as s
import reduce_entries as red

"""
This script aggregates unique (argument_id, image_id) pairs from multiple .jsonl
retrieval result files. It reads each file, extracts the relevant entries, removes
duplicates, and writes all unique records into a single JSONL output file
(argument_images_retrieval.jsonl), sorted so that entries with the same argument_id
appear together.
"""


# Directory containing the .jsonl documents
dir_with_documents = s.PROJECT_ROOT / "runs_submitted_retrieval"

# Dictionary to store unique tuples
json_dict = {}


def add_to_json(entry):
    argument_id = entry.get("argument_id")
    method = entry.get("method")
    image_id = entry.get("image_id")

    if method != "retrieval":
        raise ValueError("Method must be 'retrieval'")

    key = (argument_id, image_id)
    if key not in json_dict:
        json_dict[key] = {
            "argument_id": argument_id,
            "method": method,
            "image_id": image_id,
            "image_url": "",
        }


def save_jsonl(json_dict):
    output_file = s.PROJECT_ROOT / "argument_images_retrieval.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for key in sorted(
            json_dict.keys()
        ):  # with this sorting same arguments are together
            json_line = json.dumps(json_dict[key])
            f.write(json_line + "\n")


if __name__ == "__main__":

    # Process all .jsonl files in the directory
    for file in dir_with_documents.iterdir():
        if file.suffix == ".jsonl":
            data = red.reduce_entries(
                file
            )  # Use the reduce_top5 function to get the top 5 entries
            for entry in data:
                add_to_json(entry)
    save_jsonl(json_dict)
