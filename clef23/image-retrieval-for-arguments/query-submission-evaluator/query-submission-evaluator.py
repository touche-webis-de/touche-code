#!/usr/bin/env python3

"""Validator for the query submission sub-task of TOUCHE 2023 Task 3: Image Retrieval for Arguments"""
# Version: 2022-11-19

import argparse
import os
import re
import xml.etree.ElementTree as ElementTree

argparser = argparse.ArgumentParser(description="Validator for the query submission sub-task of TOUCHE 2023 Task 3: Image Retrieval for Arguments")
argparser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least the 'topics.xml'")
argparser.add_argument(
        "-r", "--inputRun", type=str, required=True,
        help="Directory that contains the run file in TSV format")
argparser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'evaluation.prototext' will be written: will be created if it does not exist")
args = argparser.parse_args()

def readTopics(inputDataset):
    document = ElementTree.parse(os.path.join(inputDataset, "topics.xml"))
    topics = {}
    for topicElement in document.getroot():
        topic = {}
        for topicAttributeElement in topicElement:
            topic[topicAttributeElement.tag] = topicAttributeElement.text.strip()
        topics[topic["number"]] = topic["title"]
    return topics;

def readRun(runDirectory, topics):
    run = {}
    for runFileBaseName in os.listdir(runDirectory):
        runFileName = os.path.join(runDirectory, runFileBaseName)
        if os.path.isfile(runFileName):
            with open(runFileName, "r") as runFile:
                lineCount = 0
                for line in runFile.readlines():
                    lineCount += 1
                    if lineCount != 1 or line != "number\ttopic\tproQuery\tconQuery\n":
                        parts = line.split("\t")
                        if len(parts) != 4:
                            print("Invalid line (" + str(len(parts)) + " fields instead of 4) " + str(lineCount) + ": '" + line + "'")
                            continue
                        number = parts[0].strip()
                        if re.match(r'^[1-9][0-9]*$', number) == None:
                            print("Not a topic number in line " + str(lineCount) + ": '" + number + "'")
                            continue
                        if number not in topics.keys():
                            print("Not a topic number for this dataset in line " + str(lineCount) + ": '" + number + "'")
                            continue
                        if number in run.keys():
                            print("Duplicate topic number in line " + str(lineCount) + ": '" + number + "'")
                            continue
                        topic = parts[1].strip()
                        if topic != topics[number]:
                            print("Wrong topic number '" + number + "' in line " + str(lineCount) + ": '" + topic + "' but should be '" + topics[number] + "'")
                            continue
                        proQuery = parts[2].strip()
                        conQuery = parts[3].strip()
                        run[number] = (proQuery, conQuery)
    return run

def isQuery(query):
    return query != "" and query != "PRO" and query != "CON"

def writeEvaluation(run, outputDataset):
    if not os.path.exists(outputDataset):
        os.makedirs(outputDataset)
    proQueries = 0
    conQueries = 0
    for (number, queries) in run.items():
        proQuery = queries[0]
        conQuery = queries[1]
        if isQuery(proQuery):
            proQueries += 1
        if isQuery(conQuery):
            conQueries += 1
    with open(os.path.join(outputDataset, "evaluation.prototext"), "w") as evaluationFile:
        evaluationFile.write("measure {\n key: \"proQueries\"\n value: \"" + str(proQueries) + "\"\n}\n")
        evaluationFile.write("measure {\n key: \"conQueries\"\n value: \"" + str(conQueries) + "\"\n}\n")


topics = readTopics(args.inputDataset)
writeEvaluation(readRun(args.inputRun, topics), args.outputDataset)

