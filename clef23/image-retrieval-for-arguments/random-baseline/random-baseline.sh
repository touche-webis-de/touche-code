#!/bin/bash

inputDataset=$1
outputDir=$2

for topic in $(cat $inputDataset/topics.xml | grep "<number>" | grep -o "[0-9]*");do
  for stance in PRO CON;do
    shuf $inputDataset/image-ids.txt \
      | head -n 10 \
      | awk '{printf "'$topic' '$stance' %s %d %d minscRandom\n", $1, NR, 11 - NR}'
   done
done > $outputDir/run.txt

