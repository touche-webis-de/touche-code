#!/bin/sh

#1 file with one known image ID per line: https://files.webis.de/corpora/corpora-webis/corpus-touche-image-search-22/image-ids.txt
#2 run file to check
#3 output file
awk -F' ' 'FILENAME == ARGV[1] {
  knownImageIds[$1] = 1 
} FILENAME == ARGV[2] {
  if (NF != 6) {
    printf "Invalid line %d with %d fields (not 6)\n", FNR, NF 
    next
  }

  topic = $1
  if (!(topic ~ /^[1-9][0-9]*$/ && topic <= 50)) {
    printf "Invalid line %d with invalid topic number: \"%s\"\n", FNR, topic
    next
  }

  stance = $2
  if (stance != "PRO" && stance != "CON") {
    printf "Invalid line %d with invalid stance: \"%s\"\n", FNR, stance
    next
  }

  imageId = $3
  if (!(imageId in knownImageIds)) {
    printf "Invalid line %d with unknown image ID: \"%s\"\n", FNR, imageId
    next
  }

  rank = $4
  if (!(rank ~ /^[1-9][0-9]*$/ && rank <= 10)) {
    printf "Invalid line %d with invalid rank: \"%s\"\n", FNR, rank
    next
  }
  if (rank <= highestRank[topic" "stance]) {
    printf "Invalid line %d with non-increasing rank %d for topic %d and stance %s (previous: %d)\n", FNR, rank, topic, stance, highestRank[topic" "stance]
    next
  }
  highestRank[topic" "stance] = rank

  score = $5
  if (!(score ~ /^-?[0-9]+\.?[0-9]*$/)) {
    printf "Invalid line %d with invalid score: \"%s\"\n", FNR, score
    next
  }
  if (topic" "stance in lowestScore && score > lowestScore[topic" "stance]) {
    printf "Invalid line %d with increasing score %s for topic %d and stance %s (previous: %s)\n", FNR, score, topic, stance, lowestScore[topic" "stance]
    next
  }
  lowestScore[topic" "stance] = score

  tag = $6
  if (onlyTag == "") {
    onlyTag = tag
  } else if (tag != onlyTag) {
    printf "Invalid line %d with tag \"%s\" after having encountered tag \"%s\"\n", FNR, tag, onlyTag
  }

  topics[topic] = 1
  topicDocuments[topic] += 1
} END {
  minimumDocumentsPerTopic = 20
  averageDocumentsPerTopic = 0
  for (topic in topics) {
    numTopics += 1
    numDocuments = topicDocuments[topic]
    totalDocuments += numDocuments 
    if (numDocuments < minimumDocumentsPerTopic) {
      minimumDocumentsPerTopic = numDocuments
    }
    if (numDocuments > maximumDocumentsPerTopic) {
      maximumDocumentsPerTopic = numDocuments
    }
  }
  if (numTopics == 0) {
    minimumDocumentsPerTopic = 0
  } else {
    averageDocumentsPerTopic = totalDocuments / numTopics
  }

  output = "'$3'"
  printf "measure {\n key: \"topicsRetrieved\"\n value: \"%d\"\n}\n", numTopics > output
  printf "measure {\n key: \"minimumDocumentsPerTopic\"\n value: \"%d\"\n}\n", minimumDocumentsPerTopic > output
  printf "measure {\n key: \"maximumDocumentsPerTopic\"\n value: \"%d\"\n}\n", maximumDocumentsPerTopic > output
  printf "measure {\n key: \"averageDocumentsPerTopic\"\n value: \"%.2f\"\n}\n", averageDocumentsPerTopic > output
}' $1 $2

