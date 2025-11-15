import xml.etree.ElementTree as ET
from pathlib import Path

"""
This script extracts all argument IDs from arguments.xml, removes duplicates,
and writes the unique IDs to argument_ids_list.txt. It also prints the total
and unique ID counts for verification.
"""

input_filename = Path.cwd() / "arguments.xml"
with open(input_filename, "r") as file:
    xml_data = file.read()

# Parse the XML data
root = ET.fromstring(xml_data)

# Extract all 'id' elements
ids = [argument.find("id").text for argument in root.findall("argument")]

print(f"Number of IDs: {len(ids)}")
# Remove duplicates by converting to a set and back to a list
ids = list(set(ids))
print(f"Number of unique IDs: {len(ids)}")

# Specify the output filename
output_filename = Path.cwd() / "argument_ids_list.txt"

# Write the list of ids to a file
with open(output_filename, "w") as file:
    for id_value in ids:
        file.write(f"{id_value}\n")

print(f"IDs have been written to {output_filename}")
