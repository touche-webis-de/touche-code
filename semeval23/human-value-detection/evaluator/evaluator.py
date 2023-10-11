#!/usr/bin/env python3

"""Evaluator for Human Value Detection 2023 @ Touche and SemEval 2023"""
# Version: 2023-08-13

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
argparser.add_argument("--accuracy", action="store_true")
args = argparser.parse_args()

# level 1
# availableValues = [ "Be ambitious", "Be behaving properly", "Be broadminded", "Be capable", "Be choosing own goals", "Be compliant", "Be courageous", "Be creative", "Be curious", "Be daring", "Be forgiving", "Be helpful", "Be holding religious faith", "Be honest", "Be honoring elders", "Be humble", "Be independent", "Be intellectual", "Be just", "Be logical", "Be loving", "Be neat and tidy", "Be polite", "Be protecting the environment", "Be respecting traditions", "Be responsible", "Be self-disciplined", "Have a comfortable life", "Have a good reputation", "Have an exciting life", "Have an objective view", "Have a safe country", "Have a sense of belonging", "Have a stable society", "Have a varied life", "Have a world at peace", "Have a world of beauty", "Have equality", "Have freedom of action", "Have freedom of thought", "Have good health", "Have harmony with nature", "Have influence", "Have life accepted as is", "Have loyalty towards friends", "Have no debts", "Have pleasure", "Have privacy", "Have social recognition", "Have success", "Have the own family secured", "Have the right to command", "Have the wisdom to accept others", "Have wealth" ]
# level 2
availableValues = [ "Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance", "Universalism: objectivity" ]

def readLabels(directory, prefix = None, availableArgumentIds = None):
    labels = {}
    for labelsBaseName in os.listdir(directory):
        if labelsBaseName.endswith(".tsv"):
            if prefix == None or labelsBaseName.startswith(prefix):
                labelsFileName = os.path.join(directory, labelsBaseName)
                with open(labelsFileName, "r", newline='', encoding='utf-8-sig') as labelsFile:
                    print("Reading " + labelsFileName)
                    reader = csv.DictReader(labelsFile, delimiter = "\t")
                    if "Argument ID" not in reader.fieldnames:
                        print("Skipping file " + labelsFileName + " due to missing field 'Argument ID'")
                        print(reader.fieldnames)
                        continue
                    invalidFieldNames = False
                    for fieldName in reader.fieldnames:
                        if fieldName != "Argument ID" and fieldName not in availableValues:
                            print("Skipping file " + labelsFileName + " due to invalid field '" + fieldName + "'; available field names: " + str(availableValues))
                            invalidFieldNames = True
                            break
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
                        has_invalid_labels = False
                        for label in row.values():
                            if label != "0" and label != "1":
                                print("Skipping line " + str(lineNumber) + " due to invalid label '" + label + "'")
                                has_invalid_labels = True
                                break
                        if has_invalid_labels:
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
    trueNegatives = initializeCounter()

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
            else:
                if truthLabels[argumentId][value] == "0":
                    trueNegatives[value] += 1

    with open(os.path.join(outputDataset, "evaluation.prototext"), "w") as evaluationFile:
        precisions = []
        recalls = []
        fmeasures = []
        accuracies = []
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
                accuracy = 0
                hits = truePositives[value] + trueNegatives[value]
                if hits > 0:
                    accuracy = hits / numInstances 
                accuracies.append(accuracy)
        precision = sum(precisions) / len(precisions)
        recall = sum(recalls) / len(recalls)
        fmeasure = 2 * precision * recall / (precision + recall)
        accuracy = sum(accuracies) / len(accuracies)

        evaluationFile.write("measure {\n key: \"F1\"\n value: \"" + str(fmeasure) + "\"\n}\n")
        evaluationFile.write("measure {\n key: \"Precision\"\n value: \"" + str(precision) + "\"\n}\n")
        evaluationFile.write("measure {\n key: \"Recall\"\n value: \"" + str(recall) + "\"\n}\n")
        if args.accuracy:
            evaluationFile.write("measure {\n key: \"Accuracy\"\n value: \"" + str(accuracy) + "\"\n}\n")
        skippedValues = 0
        for v in range(len(availableValues)):
            value = availableValues[v]
            if relevants[value] == 0:
                skippedValues += 1
            else:
                evaluationFile.write("measure {\n key: \"Precision " + value + "\"\n value: \"" + str(precisions[v - skippedValues]) + "\"\n}\n")
                evaluationFile.write("measure {\n key: \"Recall " + value + "\"\n value: \"" + str(recalls[v - skippedValues]) + "\"\n}\n")
                evaluationFile.write("measure {\n key: \"F1 " + value + "\"\n value: \"" + str(fmeasures[v - skippedValues]) + "\"\n}\n")
                if args.accuracy:
                    evaluationFile.write("measure {\n key: \"Accuracy " + value + "\"\n value: \"" + str(accuracies[v - skippedValues]) + "\"\n}\n")

writeEvaluation(readLabels(args.inputDataset, prefix="labels-"), readLabels(args.inputRun), args.outputDataset)

