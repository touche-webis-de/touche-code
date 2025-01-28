from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import json
import ast

args_embedding_csv = '../../indexing/argument_embeddings.csv'
args_xml = '../../indexing/arguments.xml'
load_dotenv()

# Access the password
password = os.getenv("ELASTICSEARCH_PASSWORD")  # set the password in the .env file if needed

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", password)
)

INDEX_NAME = "image_dataset"


def search_similar_images(argument_embedding, top_n=5):
    query = {
        "size": top_n,
        "query": {
            "knn": {
                "field": "image_embedding",
                "query_vector": argument_embedding,
                "k": top_n
            }
        }
    }

    response = es.search(index=INDEX_NAME, body=query)

    results = []
    for rank, hit in enumerate(response["hits"]["hits"], start=1):
        source = hit["_source"]
        results.append({
            "score": hit["_score"],
            "image_id": source.get("image_id", "N/A"),
            "image_url": source.get("image_url", "N/A"),
            "caption": source.get("image_caption", "N/A"),
            "rank": rank
        })

    return results

def save_results_to_jsonl(results, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')


def get_results(arguments):
    all_results = []
    for _, row in arguments.iterrows():
        argument_id = row['argument_id']
        argument_embedding = row['argument_embedding']

        # Convert string representation of list to actual list
        try:
            argument_embedding = np.fromstring(argument_embedding.strip('[]'), sep=' ')
        except (ValueError, SyntaxError) as e:
            print(f"Error converting argument_embedding: {e}")
            continue

        results = search_similar_images(argument_embedding.tolist())
        all_results.append({
            "argument_id": argument_id,
            "method": "retrieval",
            "image_id": results[0]["image_id"] if results else "N/A",
            "rationale": "OPTIONAL",
            "rank": results[0]["rank"] if results else "N/A",
            "tag": "bm25-baseline"
        })
    
    return all_results

# main logic
if __name__ == "__main__":
    print("\n### Baseline-Verfahren: Searching for similar images ###")

    # Load argument embeddings from CSV file
    arguments = pd.read_csv(args_embedding_csv)

    # get the results
    all_results = get_results(arguments)

    # Save results
    save_results_to_jsonl(all_results, "results.jsonl")

    print("Results saved to results.jsonl")