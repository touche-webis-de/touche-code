#!/usr/bin/env python3

"""Evaluator for Human Value Detection 2023 @ Touche and SemEval 2023"""
# Version: 2022-11-27

import argparse
import csv
import os

argparser = argparse.ArgumentParser(description="Evaluator for Human Value Detection 2023 @ Touche and SemEval 2023")
argparser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least the 'labels-*.tsv'")
argparser.add_argument(
        "-r", "--inputRun", type=str, required=True,
        help="Directory that contains the run file in TSV format")
argparser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'evaluation.prototext' will be written: will be created if it does not exist")
args = argparser.parse_args()

availableValues = [ "Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance", "Universalism: objectivity" ]

def readLabels(directory, prefix = None, availableArgumentIds = None):
    labels = {}
    for labelsBaseName in os.listdir(directory):
        if labelsBaseName.endswith(".tsv"):
            if prefix == None or labelsBaseName.startswith(prefix):
                labelsFileName = os.path.join(directory, labelsBaseName)
                with open(labelsFileName, "r", newline='') as labelsFile:
                    print("Reading " + labelsFileName)
                    reader = csv.DictReader(labelsFile, delimiter = "\t")
                    if "Argument ID" not in reader.fieldnames:
                        print("Skipping file " + labelsFileName + " due to missing field 'Argument ID'")
                        continue
                    invalidFieldNames = False
                    for fieldName in reader.fieldnames:
                        if fieldName != "Argument ID" and fieldName not in availableValues:
                            print("Skipping file " + labelsFileName + " due to invalid field '" + fieldName + "'; available field names: " + str(availableValues))
                            invalidFieldNames = True
                    if invalidFieldNames:
                        continue

                    lineNumber = 1
                    for row in reader:
                        lineNumber += 1
                        argumentId = row["Argument ID"]
                        if availableArgumentIds != None and argumentId not in availableArgumentIds:
                            print("Skipping line " + str(lineNumber) + " due to unknown Argument ID '" + argumentId + "'")
                            continue
                        del row["Argument ID"]
                        for label in row.values():
                            if label != "0" and label != "1":
                                print("Skipping line " + str(lineNumber) + " due to invalid label '" + label + "'")
                                continue
                        labels[argumentId] = row
    if len(labels) == 0:
        if prefix == None:
            raise OSError("No labels found in directory '" + directory + "'")
        else:
            raise OSError("No '" + prefix + "' labels found in directory '" + directory + "'")
    return labels

def initializeCounter():
    counter = {}
    for value in availableValues:
        counter[value] = 0
    return counter

def writeEvaluation(truthLabels, runLabels, outputDataset):
    numInstances = len(truthLabels)
    print("Truth labels: " + str(numInstances))
    print("Run labels:   " + str(len(runLabels)))

    if not os.path.exists(outputDataset):
        os.makedirs(outputDataset)

    relevants = initializeCounter()
    positives = initializeCounter()
    truePositives = initializeCounter()

    for (argumentId, labels) in truthLabels.items():
        for (value, label) in labels.items():
            if label == "1":
                relevants[value] += 1

    for (argumentId, labels) in runLabels.items():
        for (value, label) in labels.items():
            if label == "1":
                positives[value] += 1
                if truthLabels[argumentId][value] == "1":
                    truePositives[value] += 1

    with open(os.path.join(outputDataset, "evaluation.prototext"), "w") as evaluationFile:
        precisions = []
        recalls = []
        fmeasures = []
        for value in availableValues:
            if relevants[value] != 0:
                precision = 0
                if positives[value] != 0:
                    precision = truePositives[value] / positives[value]
                precisions.append(precision)
                recall = truePositives[value] / relevants[value]
                recalls.append(recall)
                fmeasure = 0
                if precision + recall != 0:
                    fmeasure = 2 * precision * recall / (precision + recall)
                fmeasures.append(fmeasure)
        precision = sum(precisions) / len(precisions)
        recall = sum(recalls) / len(recalls)
        fmeasure = 2 * precision * recall / (precision + recall)

        evaluationFile.write("measure {\n key: \"F1\"\n value: \"" + str(fmeasure) + "\"\n}\n")
        evaluationFile.write("measure {\n key: \"Precision\"\n value: \"" + str(precision) + "\"\n}\n")
        evaluationFile.write("measure {\n key: \"Recall\"\n value: \"" + str(recall) + "\"\n}\n")
        skippedValues = 0
        for v in range(len(availableValues)):
            value = availableValues[v]
            if relevants[value] == 0:
                skippedValues += 1
            else:
                evaluationFile.write("measure {\n key: \"Precision " + value + "\"\n value: \"" + str(precisions[v - skippedValues]) + "\"\n}\n")
                evaluationFile.write("measure {\n key: \"Recall " + value + "\"\n value: \"" + str(recalls[v - skippedValues]) + "\"\n}\n")
                evaluationFile.write("measure {\n key: \"F1 " + value + "\"\n value: \"" + str(fmeasures[v - skippedValues]) + "\"\n}\n")

writeEvaluation(readLabels(args.inputDataset, prefix="labels-"), readLabels(args.inputRun), args.outputDataset)

