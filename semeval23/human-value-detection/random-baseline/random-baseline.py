#!/usr/bin/env python3

"""Random baseline for Human Value Detection 2023 @ Touche and SemEval 2023"""
# Version: 2022-11-21

import argparse
import csv
import os
import random

argparser = argparse.ArgumentParser(description="Random baseline for Human Value Detection 2023 @ Touche and SemEval 2023")
argparser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least one arguments file with '.tsv' suffix")
argparser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'run.tsv' will be written: will be created if it does not exist")
args = argparser.parse_args()

# level 1
# values = [ "Be ambitious", "Be behaving properly", "Be broadminded", "Be capable", "Be choosing own goals", "Be compliant", "Be courageous", "Be creative", "Be curious", "Be daring", "Be forgiving", "Be helpful", "Be holding religious faith", "Be honest", "Be honoring elders", "Be humble", "Be independent", "Be intellectual", "Be just", "Be logical", "Be loving", "Be neat and tidy", "Be polite", "Be protecting the environment", "Be respecting traditions", "Be responsible", "Be self-disciplined", "Have a comfortable life", "Have a good reputation", "Have an exciting life", "Have an objective view", "Have a safe country", "Have a sense of belonging", "Have a stable society", "Have a varied life", "Have a world at peace", "Have a world of beauty", "Have equality", "Have freedom of action", "Have freedom of thought", "Have good health", "Have harmony with nature", "Have influence", "Have life accepted as is", "Have loyalty towards friends", "Have no debts", "Have pleasure", "Have privacy", "Have social recognition", "Have success", "Have the own family secured", "Have the right to command", "Have the wisdom to accept others", "Have wealth" ]
# probabilities = [ 0.03, 0.05, 0.12, 0.12, 0.11, 0.16, 0.02, 0.01, 0.03, 0.01, 0.03, 0.05, 0.12, 0.16, 0.06, 0.01, 0.08, 0.05, 0.12, 0.05, 0.03, 0.08, 0.12, 0.06, 0.00, 0.19, 0.20, 0.22, 0.08, 0.05, 0.13, 0.03, 0.12, 0.03, 0.01, 0.01, 0.07, 0.14, 0.04, 0.02, 0.05, 0.03, 0.15, 0.00, 0.16, 0.24, 0.09, 0.05, 0.06, 0.01, 0.09, 0.06, 0.10, 0.13 ]
# level 2
values = [ "Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance", "Universalism: objectivity" ]
probabilities = [ 0.17, 0.26, 0.06, 0.04, 0.27, 0.09, 0.11, 0.07, 0.38, 0.31, 0.11, 0.23, 0.04, 0.08, 0.29, 0.15, 0.38, 0.07, 0.14, 0.18 ]

# "instance" is a dict with keys "Argument ID", "Conclusion", "Stance", and "Premise"
# return value is the list of detected values (here: random)
def labelInstance(instance):
    instanceValues = []
    for v in range(len(values)):
        if random.random() <= probabilities[v]:
            instanceValues.append(values[v])
    return instanceValues

# generic code for reading and writing

def readInstances(directory):
    instances = []
    for instancesBaseName in os.listdir(directory):
        if instancesBaseName.startswith("arguments") and instancesBaseName.endswith(".tsv"):
            instancesFileName = os.path.join(directory, instancesBaseName)
            with open(instancesFileName, "r", newline='') as instancesFile:
                print("Reading " + instancesFileName)
                reader = csv.DictReader(instancesFile, delimiter = "\t")
                for fieldName in ["Argument ID", "Conclusion", "Stance", "Premise"]:
                    if fieldName not in reader.fieldnames:
                        print("Skipping file " + instancesFileName + " due to missing field '" + fieldName + "'")
                        continue
                for row in reader:
                    instances.append(row)
    return instances;

def labelInstances(instances):
    print("Labeling " + str(len(instances)) + " instances")
    labels = {}
    for instance in instances:
        labels[instance["Argument ID"]] = labelInstance(instance)
    return labels

def writeRun(labels, outputDataset):
    if not os.path.exists(outputDataset):
        os.makedirs(outputDataset)

    usedValues = set()
    for instanceValues in labels.values():
        usedValues.update(instanceValues)

    for usedValue in usedValues:
        if usedValue not in values:
            print("Unknown value: '" + usedValue + "'")
            exit(1)

    print("Detected values: " + str(usedValues))

    fieldNames = [ "Argument ID" ]
    for value in values:
        if value in usedValues:
            fieldNames.append(value)

    print("Writing run file")
    with open(os.path.join(outputDataset, "run.tsv"), "w") as runFile:
        writer = csv.DictWriter(runFile, fieldnames = fieldNames, delimiter = "\t")
        writer.writeheader()
        for (argumentId, instanceValues) in labels.items():
            row = { "Argument ID": argumentId }
            for value in usedValues:
                if value in instanceValues:
                    row[value] = "1"
                else:
                    row[value] = "0"
            writer.writerow(row)

writeRun(labelInstances(readInstances(args.inputDataset)), args.outputDataset)

