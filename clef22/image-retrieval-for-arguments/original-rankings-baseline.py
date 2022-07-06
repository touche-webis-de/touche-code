#!/usr/bin/env python3

"""Original Rankings Baseline for TOUCHE 2022 Task 3: Image Retrieval for Arguments"""
# Version: 2021-12-13

import argparse
import json
import os


argparser = argparse.ArgumentParser(description="Original Rankings Baseline for TOUCHE 2022 Task 3: Image Retrieval for Arguments")
argparser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least the 'images' directory and the 'topics.xml'")
argparser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'run.txt' will be written: will be created if it does not exist")
args = argparser.parse_args()



def readRankings(inputDataset):
    rankings = {}
    def addToRankings(topic, imageId, stance, rank):
        if not topic in rankings:
            rankings[topic] = {}
        if not imageId in rankings[topic] or rankings[topic][imageId]["rank"] > rank:
            rankings[topic][imageId] = {"stance": stance, "rank": rank, "imageId": imageId}

    imagesDirectory = os.path.join(inputDataset, "images")
    for imageShortId in os.listdir(imagesDirectory):
        for imageId in os.listdir(os.path.join(imagesDirectory, imageShortId)):
            imageDirectory = os.path.join(imagesDirectory, imageShortId, imageId)
            pagesDirectory = os.path.join(imageDirectory, "pages")
            for pageId in os.listdir(pagesDirectory):
                with open(os.path.join(pagesDirectory, pageId, "rankings.jsonl"), "r") as rankingsFile:
                    lines = list(rankingsFile)
                for line in lines:
                    ranking = json.loads(line)
                    if ranking["query"].endswith(" good"):
                        addToRankings(ranking["topic"], imageId, "PRO", ranking["rank"])
                    elif ranking["query"].endswith(" anti"):
                        addToRankings(ranking["topic"], imageId, "CON", ranking["rank"])

    return rankings



def writeTopRankings(rankings, outputDataset):
    if not os.path.exists(outputDataset):
        os.makedirs(outputDataset)
    with open(os.path.join(outputDataset, "run.txt"), "w") as runFile:

        def printResults(topic, ranking, stance):
            rank = 1
            for result in ranking:
                if result["stance"] == stance:
                    line = "%d %s %s %d %.2f minsk-original" % (int(topic), stance, result["imageId"], rank, (101 - result["rank"]) / 100)
                    runFile.write(line + "\n")
                    rank += 1
                    if rank > 10:
                        break

        for topic in sorted(list(rankings.keys()), key=int):
            ranking = sorted(list(rankings[topic].values()), key=lambda x : x["rank"])
            printResults(topic, ranking, "PRO")
            printResults(topic, ranking, "CON")



writeTopRankings(readRankings(args.inputDataset), args.outputDataset)

