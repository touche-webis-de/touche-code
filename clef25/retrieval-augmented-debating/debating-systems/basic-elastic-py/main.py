from elasticsearch import Elasticsearch
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

client = Elasticsearch('https://touche25-rad.webis.de/arguments')
index = "claimrev"

# Types
class Message(BaseModel):
    role: str
    content: str

class Request(BaseModel):
    messages: List[Message]


def reply(messages: List[Message]):
    """
    Continues the conversation.

    Args:
        messages: The conversation so far
    
    Returns:
        str: The response text
        List: The list of arguments that were used to generate that response, each an object with at least the collection "id"
    """
    claim = messages[-1].content
    top_result = next(query_elastic(claim))
    return top_result["text"], [ top_result ]


def query_elastic(claim, size=1):
    """
    Simple function to query the RAD Elasticsearch server.

    Args:
      claim: The claim to be rebutted
      size: The amount of results to retrieve

    Returns:
      Generator of result objects
    """
    # see https://elasticsearch-py.readthedocs.io/en/v8.17.0/api/elasticsearch.html#elasticsearch.client.Elasticsearch.search
    response = client.search(index=index, query={
            "match": {
                "attacks": {
                    "query": claim
                }
            }
        }, source_excludes=["text_embedding_stella", "supports_embedding_stella", "attacks_embedding_stella"], size=size)
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
    content, arguments = reply(request.messages)
    return {
        "content": content,
        "arguments": arguments
    }

