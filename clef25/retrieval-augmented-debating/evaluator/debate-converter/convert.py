from pydantic import BaseModel
from typing import List
import json

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
    userTurns: List[UserTurn]

class Run(BaseModel):
    simulation: Simulation


with open("touche25-rad-cmv-debates.jsonl") as f:
    debates = [json.loads(line) for line in f if line != ""]

for debate in debates:
    num_turns = len(debate["debate"])
    userTurns = []
    for i in range(1, num_turns, 2):
        userUtterance = debate["debate"][i-1]["content"]
        systemUtterance = debate["debate"][i]["content"]
        systemArguments = []
        for argument in debate["debate"][i]["arguments"]:
            systemArguments.append(Argument(**argument))
        userTurns.append(UserTurn(
            utterance=userUtterance,
            systemResponse=SystemResponse(
                utterance=systemUtterance,
                response=RetrievalResponse(
                    arguments=systemArguments
                )
            )))
    run = Run(simulation=Simulation(userTurns=userTurns))
    print(run.model_dump_json())
