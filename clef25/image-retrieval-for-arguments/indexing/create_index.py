### Indexing ###

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import json
import clip
import torch
from PIL import Image

load_dotenv()
# start the elastic container with the following command: curl -fsSL https://elastic.co/start-local | sh
# then copy the password into the .env file
password = os.getenv("ELASTICSEARCH_PASSWORD") # set the password in the .env file

es = Elasticsearch(
    "http://localhost:9200",   
    basic_auth=("elastic", password), 
)

print(es.ping())

# Load CLIP model and preprocessing pipeline for image embeddings
device = torch.device("cpu")  # Use "cpu", "mps" (for Apple Silicon), or "cuda" (for GPU)
model, preprocess = clip.load("ViT-B/32", device=device)

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
            }
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
    image_embedding = create_embedding(image_dir, "image.webp")
    
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
                "image_embedding": image_embedding
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


# create the embedding for one image
def create_embedding(root, file):
    image_vector = []
    if file.lower().endswith(".webp"):
        file_path = os.path.join(root, file)
        try:
            # Load and preprocess the image
            image = preprocess(Image.open(file_path)).unsqueeze(0).to(device)
            
            # Generate the embedding
            with torch.no_grad():
                image_features = model.encode_image(image)
            
            image_vector = image_features.cpu().numpy()
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return image_vector



index_dataset(BASE_PATH)

print("Indexing completed.")



