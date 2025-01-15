from elasticsearch import Elasticsearch
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

client = Elasticsearch('https://touche25-rad.webis.de/arguments')
index = "claimrev"

# Types
class Message(BaseModel):
    role: str
    content: str

class Request(BaseModel):
    messages: List[Message]


# Basic Elasticsearch System
def reply(messages: List[Message]) -> str:
    claim = messages[-1].content
    top_result = next(query_elastic(claim))
    print(top_result)
    return top_result["text"]


# Simple function to query the RAD Elasticsearch server
def query_elastic(claim, size=1):
    response = client.search(index=index, query={
            "match": {
                "attacks": {
                    "query": claim
                }
            }
        }, source_excludes=["text_embedding_stella", "supports_embedding_stella", "attacks_embedding_stella"])
    rank = 1
    for hit in response["hits"]["hits"]:
        result = hit["_source"]
        result["key"] = rank
        result["id"] = hit["_id"]
        result["score"] = hit["_score"]
        rank += 1
        yield result

# Simple application server -- no need to touch this code if you extend this system
app = FastAPI()

@app.post("/")
async def respond(request: Request):
    return {
        "message": {
            "role": "assistant",
            "content": reply(request.messages)
        }
    }

