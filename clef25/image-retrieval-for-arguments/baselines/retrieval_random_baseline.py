import xml.etree.ElementTree as ET
import json
import random

# project root is image-retrieval-for-arguments
import validator.settings as s

def main():

    random.seed(42)

    image_id_list = []
    with open(s.PROJECT_ROOT / "image_id_list.txt", "r") as file :
        image_id_list = [line.strip() for line in file.readlines()]

    xml_data = None
    arguments_xml = s.PROJECT_ROOT / "arguments.xml"
    with open(arguments_xml, "r") as file:
        xml_data = file.read()

    # Parse the XML data
    root = ET.fromstring(xml_data)

    argument_tuples = []
    for argument in root.findall('argument'):
        arg_id = argument.find('id').text if argument.find('id') is not None else None
        claim = argument.find('claim').text if argument.find('claim') is not None else None
        argument_tuples.append((arg_id, claim))

    tag = "touche25-baseline-random"
    method = "retrieval"
    final_files = []

    for r in argument_tuples:
        id = r[0]
        argument = r[1]
        for i in range(1, 6):
            image_id = random.choice(image_id_list)
            argument_entry = {
                "argument_id": id,
                "method": method,
                "image_id": image_id,
                "prompt": argument,
                "rank": i,
                "tag": tag
            }
            final_files.append(argument_entry)

    output_filename = s.PROJECT_ROOT / "retrieve_random.jsonl"
    with open(output_filename, "w") as jsonl_file:
        for entry in final_files:
            jsonl_file.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    main()











