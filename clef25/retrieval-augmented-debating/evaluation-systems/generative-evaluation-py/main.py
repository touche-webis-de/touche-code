from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

# Types
class SystemResponse(BaseModel):
    utterance: str
    results: List[Dict] | None = None
    resultsPage: str | None = None

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

@app.post("/quantity")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return {"score":None}
    return {
        "score": 1
    }

@app.post("/quality")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return {"score":None}
    return {
        "score": 1
    }

@app.post("/relation")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return {"score":None}
    return {
        "score": 1
    }

@app.post("/manner")
async def respond(request: Request):
    if request.userTurnIndex == None:
        # overall conversation evaluation not part of this task
        return {"score":None}
    return {
        "score": 1
    }
