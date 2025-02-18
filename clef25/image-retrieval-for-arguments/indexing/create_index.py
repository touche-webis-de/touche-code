### Indexing ###

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import pandas as pd
import json
import numpy as np
import re

load_dotenv()
# start the elastic container with the following command: curl -fsSL https://elastic.co/start-local | sh
# then copy the password into the .env file
password = os.getenv("ELASTICSEARCH_PASSWORD") # set the password in the .env file

es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", password))

print(es.ping())


INDEX_NAME = "image_dataset"

# define mapping for the index
index_mapping = {
    "mappings": {
        "properties": {
            "image_id": {"type": "keyword"},
            "image_url": {"type": "text"},
            "image_caption": {"type": "text"},
            "image_text": {"type": "text"},
            "image_embedding": {            # CLIP image embedding
                "type": "dense_vector",  
                "dims": 512
            },
            "website_text": {"type": "text"}
        }
    }
}

#delete index if existes and create new one
es.options(ignore_status=[400, 404]).indices.delete(index=INDEX_NAME)
es.indices.create(index=INDEX_NAME, body=index_mapping)


BASE_PATH = "./images" 

def index_dataset(base_path):
    for prefix_dir in os.listdir(base_path):
        prefix_path = os.path.join(base_path, prefix_dir)
        if os.path.isdir(prefix_path): 
            for image_hash_dir in os.listdir(prefix_path):
                image_dir = os.path.join(prefix_path, image_hash_dir)
                if os.path.isdir(image_dir): 
                    process_image_folder(image_dir)



def process_image_folder(image_dir):
    image_id = os.path.basename(image_dir) 
    image_url = load_file(os.path.join(image_dir, "image-url.txt"))
    image_caption = load_file(os.path.join(image_dir, "image-caption.txt"))
    image_text = load_file(os.path.join(image_dir, "image-text.txt"))
    image_embedding = load_embedding(image_dir)
    
    # Process web pages
    pages_dir = os.path.join(image_dir, "pages")
    if os.path.isdir(pages_dir):
        for page_hash_dir in os.listdir(pages_dir):
            page_dir = os.path.join(pages_dir, page_hash_dir)
            dir = os.path.join(page_dir, "snapshot")
            if os.path.isdir(dir):
                website_text = load_file(os.path.join(dir, "text.txt"))
            
            # Prepare document
            document = {
                "image_id": image_id,
                "image_url": image_url,
                "image_caption": image_caption,
                "image_text": image_text,
                "image_embedding": image_embedding,
                "website_text": website_text
            }
            
            # Elasticsearch indexing
            es.index(index=INDEX_NAME, id=image_id, body=document)
            print(f"Indexed: {image_id}")


def load_file(filepath):
    """help-function: reading text-files"""
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def load_json(filepath):
    """help-function: reading json-files"""
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def load_jsonl(filepath):
    """help-function: reading jsonl-files"""
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return [json.loads(line.strip()) for line in f]
    return []


# load the embeddings from csv file by image_id
def load_embedding(root):
    embedding_df = pd.read_csv("image_embeddings.csv")
    matching_row = embedding_df.loc[embedding_df['image_id'] == os.path.basename(root)]
    
    if not matching_row.empty:
        # Convert the string representation of the embedding to a list of floats
        embedding_str = matching_row['image_embedding'].values[0]  # Get the string value
        embedding_list = embedding_str.split(" ")

        flat_list = [re.sub(r'[\[\]\n]', '', item) for sublist in embedding_list for item in sublist.split()]
        flat_list = [item for item in flat_list if item]
        float_values = [float(x) for x in flat_list]
        return float_values


    else:
        # Handle the case where no matching row is found
        return None



if __name__ == "__main__":
    index_dataset(BASE_PATH)

    print("Indexing completed.")



