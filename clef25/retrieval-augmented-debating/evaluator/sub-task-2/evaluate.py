from enum import IntEnum
from pydantic import BaseModel, TypeAdapter
from typing import List
import argparse
import os
import glob

parser = argparse.ArgumentParser(
    description="Evaluator for Retrieval-Augmented Debating 2025 Sub-Task 2 @ CLEF 2025")
parser.add_argument(
    "-i", "--inputDataset", type=str, required=True,
    help="Directory that contains the input dataset, at least the '*-labels.jsonl'")
parser.add_argument(
    "-r", "--inputRun", type=str, required=True,
    help="Directory that contains the run file in JSONL format")
parser.add_argument(
    "-o", "--outputDataset", type=str, required=True,
    help="Directory to which the 'evaluation.prototext' will be written: will be created if it does not exist")
args = parser.parse_args()

# Types run file
class Evaluation(BaseModel):
    score: float

class TurnEvaluations(BaseModel):
    Quantity: Evaluation
    Quality: Evaluation
    Relation: Evaluation
    Manner: Evaluation

class DebateEvaluations(BaseModel):
    userTurnsEvaluations: List[TurnEvaluations]

# Types ground-truth
class Label(IntEnum):
    no = 0
    yes = 1

class TurnLabels(BaseModel):
    quantity: Label | None = None
    quality: Label | None = None
    relation: Label | None = None
    manner: Label | None = None

debate_labels_type = TypeAdapter(List[TurnLabels])

runFiles = glob.glob(args.inputRun + "/*.jsonl")
if len(runFiles) != 1:
    raise OSError("--inputRun directory must contain exactly 1 jsonl file, but there are: " + str(runFiles))
with open(runFiles[0]) as f:
    runs = [DebateEvaluations.model_validate_json(line).userTurnsEvaluations for line in f if line != ""]

labelFiles = glob.glob(args.inputDataset + "/*-labels.jsonl")
if len(labelFiles) != 1:
    raise OSError("--inputDataset directory must contain exactly 1 -labels.jsonl file, but there are: " + str(labelFiles))
with open(labelFiles[0]) as f:
    labels = [debate_labels_type.validate_json(line) for line in f if line != ""]

num_true_positives = {"quantity":0, "quality":0, "relation":0, "manner":0}
num_true_negatives = {"quantity":0, "quality":0, "relation":0, "manner":0}
num_false_positives = {"quantity":0, "quality":0, "relation":0, "manner":0}
num_false_negatives = {"quantity":0, "quality":0, "relation":0, "manner":0}
def evaluate(dimension, label, evaluation):
    if label != None:
        if label == 1:
            if evaluation.score >= 0.5:
                num_true_positives[dimension] += 1
            else:
                num_false_negatives[dimension] += 1
        else:
            if evaluation.score >= 0.5:
                num_false_positives[dimension] += 1
            else:
                num_true_negatives[dimension] += 1

if len(runs) != len(labels):
    raise OSError("Mismatch in number of simulations; run:" + str(len(runs)) + " ; labels: " + str(len(labels)))
s = 1
for [debateEvaluations, debateLabels] in zip(runs, labels):
    if len(debateEvaluations) != len(debateLabels):
        raise OSError("Mismatch in number of turns in simulation " + str(s) + "; run:" + str(len(debateEvaluations)) + " ; labels: " + str(len(debateLabels)))
    for [turnEvaluations, turnLabels] in zip(debateEvaluations, debateLabels):
        evaluate("quantity", turnLabels.quantity, turnEvaluations.Quantity)
        evaluate("quality", turnLabels.quality, turnEvaluations.Quality)
        evaluate("relation", turnLabels.relation, turnEvaluations.Relation)
        evaluate("manner", turnLabels.manner, turnEvaluations.Manner)
    s += 1

print("true positives:  " + str(num_true_positives))
print("true negatives:  " + str(num_true_negatives))
print("false positives: " + str(num_false_positives))
print("false negatives: " + str(num_false_negatives))

def write_dimension(dimension, file):
    precision = 0 if num_true_positives[dimension] == 0 else num_true_positives[dimension] / (num_true_positives[dimension] + num_false_positives[dimension])
    recall = 0 if num_true_positives[dimension] == 0 else num_true_positives[dimension] / (num_true_positives[dimension] + num_false_negatives[dimension])
    f1 = 0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    file.write("measure {\n key: \"" + dimension + " precision\"\n value: \"" + str(precision) + "\"\n}\n")
    file.write("measure {\n key: \"" + dimension + " recall\"\n value: \"" + str(recall) + "\"\n}\n")
    file.write("measure {\n key: \"" + dimension + " f1\"\n value: \"" + str(f1) + "\"\n}\n")

with open(os.path.join(args.outputDataset, "evaluation.prototext"), "w") as evaluationFile:
    for dimension in ["quantity", "quality", "relation", "manner"]:
        write_dimension(dimension, evaluationFile)
