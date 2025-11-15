import json
import re
import reduce_entries as red
import settings as s

"""
This script collects unique (argument_id, image_id) pairs from generation runs.
It processes all JSONL files inside participant subdirectories, constructs stable
image paths, removes duplicates, and writes the consolidated results to
argument_images_generation.jsonl, sorted so that entries for the same argument
appear together.
"""

# Directory containing the .jsonl documents
dir_with_documents = s.PROJECT_ROOT / "runs_submitted_generation"

# Dictionary to store unique tuples
json_dict = {}


# Function to extract and store necessary JSON data
def add_to_json(filepath, entry):
    argument_id = entry.get("argument_id")
    method = entry.get("method")
    image_id = entry.get("image_id")

    if method != "generation":
        raise ValueError("Method must be 'generation'")

    image_url = str((filepath / "image" / image_id).relative_to(dir_with_documents))
    image_id_full = re.sub(r"\s+", "_", image_url)
    key = (argument_id, image_id_full)
    if key not in json_dict:
        json_dict[key] = {
            "argument_id": argument_id,
            "method": method,
            "image_id": image_id_full,
            "image_url": image_url,
        }


def save_jsonl(json_dict):
    output_file = s.PROJECT_ROOT / "argument_images_generation.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for key in sorted(
            json_dict.keys()
        ):  # with this sorting same arguments are together
            json_line = json.dumps(json_dict[key])
            f.write(json_line + "\n")


if __name__ == "__main__":
    # Process all .jsonl files in the directory and its subdirectories
    for participant in dir_with_documents.iterdir():
        if participant.is_dir():  # Ensure it's a directory
            for file in participant.iterdir():
                if file.suffix == ".jsonl":
                    data = red.reduce_entries(
                        file
                    )  # Use the reduce_top5 function to get the top 5 entries
                    for entry in data:
                        add_to_json(file.parent, entry)
    save_jsonl(json_dict)
