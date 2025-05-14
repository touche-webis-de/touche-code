from pathlib import Path

# Define the path to search
path_to_search = Path.cwd() / "images"
list_of_image_ids= []

# Iterate through directories and handle potential errors
if path_to_search.exists() and path_to_search.is_dir():
    for group_dir in path_to_search.iterdir():
        if group_dir.is_dir():
            for image_hash_dir in group_dir.iterdir():
                if image_hash_dir.is_dir():
                    name = image_hash_dir.name
                    list_of_image_ids.append(name)

# Print the count of files
print(f"Number of IDs: {len(list_of_image_ids)}")
# Remove duplicates by converting to a set and back to a list
ids = list(set(list_of_image_ids))
print(f"Number of unique IDs: {len(ids)}")

# Write the list to a file
output_file = Path.cwd() / "image_id_list.txt"
with output_file.open("w") as f:
    for file_name in list_of_image_ids:
        f.write(file_name + "\n")