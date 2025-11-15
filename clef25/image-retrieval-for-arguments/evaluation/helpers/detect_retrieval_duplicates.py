import json
import settings as s
from collections import defaultdict

"""
This script compares retrieval result files by converting each JSONL file into a
set of (argument_id, image_id, rank) tuples. Files with identical sets are grouped
together, allowing detection of duplicate or equivalent submissions. The script
prints groups of files that share the same content, as well as unique files.
"""


# Keys representing the essential identifiers
keys_to_check = ["argument_id", "image_id", "rank"]

# Store sets by file path
sets_dict = dict()


def create_sets_comparison(file_path):
    with open(file_path, "r") as file:
        file_content = [json.loads(line.strip()) for line in file]

    set_of_entries = set()
    for line in file_content:
        entry_tuple = tuple(line[key] for key in keys_to_check)
        set_of_entries.add(entry_tuple)

    sets_dict[file_path.name] = set_of_entries  # Use file name only for cleaner output


def group_equal_sets():
    # Use a dict where key = frozen set of entries, value = list of file names with that set
    group_map = defaultdict(list)

    for file_name, entry_set in sets_dict.items():
        group_map[frozenset(entry_set)].append(file_name)

    # Sort by group size descending
    sorted_groups = sorted(
        group_map.items(), key=lambda item: len(item[1]), reverse=True
    )

    for i, (entry_set, file_names) in enumerate(sorted_groups, 1):
        if len(file_names) > 1:
            print(f"\nGroup {i} - Equal Sets in {len(file_names)} files:")
        else:
            print(f"\nGroup {i} - Unique Set:")

        for name in sorted(file_names):
            print(f"  • {name}")
        print(f"  → Total entries in set: {len(entry_set)}")


if __name__ == "__main__":
    path_with_files = s.PROJECT_ROOT / "runs_submitted_retrieval"

    for file_path in path_with_files.iterdir():
        if file_path.suffix == ".jsonl":  # Optional: Filter by file type
            create_sets_comparison(file_path)

    group_equal_sets()
