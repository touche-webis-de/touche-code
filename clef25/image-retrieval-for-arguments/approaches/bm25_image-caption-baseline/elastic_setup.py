### Indexing ###

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import json

load_dotenv()
# start the elastic container with the following command: curl -fsSL https://elastic.co/start-local | sh
# then copy the password into the .env file
password = os.getenv("ELASTICSEARCH_PASSWORD") # set the password in the .env file

es = Elasticsearch(
    "http://localhost:9200",   
    basic_auth=("elastic", password), 
)

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
            "phash": {"type": "keyword"},
            "annotations": {"type": "nested"},
            "page_url": {"type": "text"},
            "rankings": {"type": "nested"},
            "nodes": {"type": "nested"},
        }
    }
}

# create index if not exists
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body=index_mapping)
    print(f"Index '{INDEX_NAME}' created.")
else:
    print(f"Index '{INDEX_NAME}' already exist.")

BASE_PATH = "./images" 

def index_dataset(base_path):
    for prefix_dir in os.listdir(base_path):
        prefix_path = os.path.join(base_path, prefix_dir)
        if os.path.isdir(prefix_path):  # Prüfen, ob Präfix-Ordner
            for image_hash_dir in os.listdir(prefix_path):
                image_dir = os.path.join(prefix_path, image_hash_dir)
                if os.path.isdir(image_dir):  # Prüfen, ob Bildordner
                    # Hier wird mit dem Indexieren begonnen
                    process_image_folder(image_dir)


def process_image_folder(image_dir):
    image_id = os.path.basename(image_dir)  # Ordnername = Image ID
    image_url = load_file(os.path.join(image_dir, "image-url.txt"))
    image_caption = load_file(os.path.join(image_dir, "image-caption.txt"))
    image_text = load_file(os.path.join(image_dir, "image-text.txt"))
    
    # Process web pages
    pages_dir = os.path.join(image_dir, "pages")
    if os.path.isdir(pages_dir):
        for page_hash_dir in os.listdir(pages_dir):
            page_dir = os.path.join(pages_dir, page_hash_dir)
            
            # Prepare document
            document = {
                "image_id": image_id,
                "image_url": image_url,
                "image_caption": image_caption,
                "image_text": image_text,
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


index_dataset(BASE_PATH)

print("Indexing completed.")



