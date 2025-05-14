import os
import requests
import base64
import xml.etree.ElementTree as ET
import settings as s
import json
from tqdm import tqdm


# API endpoint
IMAGE_GENERATION_API = "https://touche25-image-generation.web.webis.de/api"
IMAGE_GENERATION_API_KEY = "touche25:aD1QFMz0E8j2CpM"

def generate_images(prompt,name_to_save,output_dir, seed=None):
    response_data = send_request(prompt, seed=seed)
    if response_data == None:
        print("Could not generate images")
        return 1

    for i, image_data in  enumerate(response_data["images"], start=1):
        image_bytes = base64.b64decode(image_data)
        filepath = os.path.join(output_dir, name_to_save)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
    return 0

def send_request(prompt, seed=None):
    headers = {"Content-Type": "application/json"}
    payload = {"prompt": prompt, "api_key" : IMAGE_GENERATION_API_KEY, "nbr_images": 1, "seed" : seed}
    try:
        response = requests.post(IMAGE_GENERATION_API, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code != 200 or response_data["status"] != "success":
            print("Error: API request failed.")
            return None

        return response_data["data"]

    except requests.exceptions.RequestException as e:
        print("Error occurred while sending request:", e)
        return None


def main():
    input_filename = s.PROJECT_ROOT / "arguments.xml"
    with open(input_filename, "r") as file:
        xml_data = file.read()

    # Parse the XML data
    root = ET.fromstring(xml_data)

    argument_tuples = []
    for argument in root.findall('argument'):
        arg_id = argument.find('id').text if argument.find('id') is not None else None
        claim = argument.find('claim').text if argument.find('claim') is not None else None
        argument_tuples.append((arg_id, claim))

    tag = "touche25-baseline-argument-prompts"
    method = "generation"
    final_files = []

    total_iterations = len(argument_tuples) * 5
    with tqdm(total=total_iterations, desc="Generating Images") as pbar:
        for r in argument_tuples:
            id = r[0]
            argument = r[1]
            for i in range(1, 6):
                image_id = f"{id}_{i}.jpg".replace(" ", "_")
                output_dir = s.PROJECT_ROOT / "images_generated"
                output_dir.mkdir(parents=True, exist_ok=True)
                generate_images(argument, image_id, output_dir=output_dir)
                argument_entry = {
                    "argument_id": id,
                    "method": method,
                    "image_id": image_id,
                    "prompt": argument,
                    "rank": i,
                    "tag": tag
                }
                final_files.append(argument_entry)
                pbar.update(1)  # update progress

    output_filename = s.PROJECT_ROOT / "final_files.jsonl"
    with open(output_filename, "w") as jsonl_file:
        for entry in final_files:
            jsonl_file.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    main()











