from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
import json

load_dotenv()

# Access the password
password = os.getenv("ELASTICSEARCH_PASSWORD")  # set the password in the .env file if needed

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", password)
)

INDEX_NAME = "image_dataset"

def search_similar_images(query_text, top_n=5):
    """
    searching for similar results based on the field 'image_caption'.
    """
    # Elasticsearch-Search-Query
    query = {
        "query": {
            "match": {
                "image_caption": query_text
            }
        },
        "size": top_n
    }

    # request to Elasticsearch
    response = es.search(index=INDEX_NAME, body=query)

    # formatting results
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

#extracts every argument from the XML file and saves the id and the claim in a list
def load_arguments_from_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    arguments = []
    for arg in root.findall('.//argument'):
        arg_id = arg.find('id').text if arg.find('id') is not None else None
        claim = arg.find('claim').text if arg.find('claim') is not None else None
        arguments.append({"id": arg_id, "claim": claim})
    return arguments

def save_results_to_jsonl(results, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

# main logic
if __name__ == "__main__":
    print("\n### Baseline-Verfahren: Searching for similar images ###")

    # Load arguments from XML file
    arguments = load_arguments_from_xml("./arguments.xml")

    all_results = []
    for argument in arguments:
        results = search_similar_images(argument["claim"])
        for result in results:
            all_results.append({
                "argument_id": argument["id"],
                "method": "retrieval",
                "image_id": result["image_id"],
                #"rationale": result["caption"],
                "rationale": "OPTIONAL",
                "rank": result["rank"],
                "tag": "bm25-baseline"
            })

    # Save results to JSONL file
    save_results_to_jsonl(all_results, "results.jsonl")

    print("Results saved to results.jsonl")
