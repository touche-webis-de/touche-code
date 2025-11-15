import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import json

"""
This script merges aspect annotations from a CSV file with argument data from an XML file.
It maps each claim to its aspects, attaches those aspects to the corresponding XML arguments,
and outputs the enriched arguments as a JSONL file (arguments_aspects.jsonl).
"""


# Read CSV
df = pd.read_csv(Path.cwd() / "touche25-arguments-aspects-raw.csv")

# Clean column names (strip whitespace)
df.columns = df.columns.str.strip()

# Find duplicates in the 'Claim' column (case sensitive)
duplicates = df[df.duplicated(subset=["Claim"], keep=False)]

if not duplicates.empty:
    print("Duplicate claims found:")
    print(duplicates)
else:
    print("No duplicate claims found.")

# Create claim -> aspects dictionary
claim_aspect_dict = pd.Series(df["Aspects"].values, index=df["Claim"]).to_dict()

# Read XML file
input_filename = Path.cwd() / "arguments.xml"
with open(input_filename, "r") as file:
    xml_data = file.read()

# Parse the XML data
root = ET.fromstring(xml_data)

# Extract all arguments into list of dicts, adding 'aspects' from the dictionary
arguments_list = []
for argument in root.findall("argument"):
    claim_text = argument.find("claim").text
    aspects = claim_aspect_dict.get(claim_text, None)  # safer access
    if aspects is not None:
        aspects = aspects.split(",")  # Split aspects by semicolon
        aspects = [aspect.strip() for aspect in aspects]
    else:
        print(f"Warning: No aspects found for claim '{claim_text}'")
        aspects = []  # Default to empty list if no aspects found

    arg_dict = {
        "id": argument.find("id").text,
        "topic": argument.find("topic").text,
        "claim": claim_text,
        "aspects": aspects,
    }
    arguments_list.append(arg_dict)

# Convert to JSON string (pretty print)
output_path = Path.cwd() / "arguments_aspects.jsonl"

with open(output_path, "w", encoding="utf-8") as f:
    for entry in arguments_list:
        json_line = json.dumps(entry, ensure_ascii=False)
        f.write(json_line + "\n")
