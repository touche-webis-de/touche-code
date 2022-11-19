#!/usr/bin/env python3

"""Baselines for the query submission sub-task of TOUCHE 2023 Task 3: Image Retrieval for Arguments"""
# Version: 2022-11-19

import argparse
import re
import os
import xml.etree.ElementTree as ElementTree

argparser = argparse.ArgumentParser(description="Baselines for the query submission sub-task of TOUCHE 2023 Task 3: Image Retrieval for Arguments")
argparser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least the 'topics.xml'")
argparser.add_argument(
        "-p", "--proExpansion", type=str, required=True,
        help="Expansion text for the PRO query")
argparser.add_argument(
        "-c", "--conExpansion", type=str, required=True,
        help="Expansion text for the CON query")
argparser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'query-submission-form-task3.tsv' will be written: will be created if it does not exist")
args = argparser.parse_args()

def readTopics(inputDataset):
    document = ElementTree.parse(os.path.join(inputDataset, "topics.xml"))
    topics = []
    for topicElement in document.getroot():
        topic = {}
        for topicAttributeElement in topicElement:
            topic[topicAttributeElement.tag] = topicAttributeElement.text.strip()
        topics.append(topic)
    return topics;

stopwords = [ "a", "an", "and", "are", "be", "can", "do", "does", "in", "is", "need", "on", "or", "should", "the", "was", "we" ]

def toKeywordQuery(title):
    words = re.sub(r'[^a-z ]', '', title.lower()).split()
    return ' '.join([word for word in words if word not in stopwords])

def expandQuery(topic, expansion):
    return toKeywordQuery(topic["title"]) + " " + expansion

def writeQueries(topics, proExpansion, conExpansion, outputDataset):
    if not os.path.exists(outputDataset):
        os.makedirs(outputDataset)
    with open(os.path.join(outputDataset, "query-submission-form-task3.tsv"), "w") as submissionFile:
        submissionFile.write("number\ttopic\tproQuery\tconQuery\n")
        for topic in topics:
            proQuery = expandQuery(topic, proExpansion)
            conQuery = expandQuery(topic, conExpansion)
            submissionFile.write(topic["number"] + "\t" + topic["title"] + "\t" + proQuery + "\t" + conQuery + "\n")

writeQueries(readTopics(args.inputDataset), args.proExpansion, args.conExpansion, args.outputDataset)
