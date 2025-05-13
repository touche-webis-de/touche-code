from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

# Types
class Argument(BaseModel):
    id: str
    text: str

class RetrievalResponse(BaseModel):
    arguments: List[Argument]

class SystemResponse(BaseModel):
    utterance: str
    response: RetrievalResponse

class UserTurn(BaseModel):
    utterance: str
    systemResponse: SystemResponse

class Simulation(BaseModel):
    configuration: Dict
    userTurns: List[UserTurn]

class Request(BaseModel):
    simulation: Simulation
    userTurnIndex: int | None = None

app = FastAPI()

# Endpoints, one for each dimension

@app.post("/quantity")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return { "score": None }
    return {
        "score": 1
    }

@app.post("/quality")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return { "score": None }
    return {
        "score": 1
    }

@app.post("/relation")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return { "score": None }
    return {
        "score": 1
    }

@app.post("/manner")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return { "score": None }
    return {
        "score": 1
    }
