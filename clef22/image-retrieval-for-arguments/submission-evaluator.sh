#!/bin/sh

#1 qrels file
#2 run file to check
#3 output file
awk -F' ' 'FILENAME == ARGV[1] {
  topic = $1
  question = $2
  imageId = $3

  items[topic" "imageId] = 1
  qrels[topic" "imageId" "question] = $4
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
  if (!(imageId ~ "^I[0-9a-f]{16}$")) {
    printf "Invalid line %d with invalid image ID: \"%s\"\n", FNR, imageId
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

  if (!(topic" "imageId in items)) {
    printf "Image %s not scored for topic %s, assuming off-topic\n", imageId, topic
  } else {
    if (qrels[topic" "imageId" ONTOPIC"] == 1) {
      correctOnTopic[topic] += 1
      correctOnTopic[topic" "stance] += 1
      correctOnTopicAll += 1
      if (qrels[topic" "imageId" "stance] == 1) {
        correctArgumentative[topic] += 1
        correctArgumentative[topic" "stance] += 1
        correctArgumentativeAll += 1
        correctStance[topic] += 1
        correctStance[topic" "stance] += 1
        correctStanceAll += 1
      } else if (qrels[topic" "imageId" PRO"] == 1 || qrels[topic" "imageId" CON"] == 1) {
        correctArgumentative[topic] += 1
        correctArgumentative[topic" "stance] += 1
        correctArgumentativeAll += 1
      }
    }
  }
  topics[topic] = 1
} END {

  PROCINFO["sorted_in"] = "@ind_num_asc"
  printf "topic,onTopic,argumentative,onStance,onTopicPro,argumentativePro,onStancePro,onTopicCon,argumentativeCon,onStanceCon\n"
  for (topic in topics) {
    numTopics += 1
    printf "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", topic, correctOnTopic[topic] / 20, correctArgumentative[topic] / 20, correctStance[topic] / 20, correctOnTopic[topic" PRO"] / 10, correctArgumentative[topic" PRO"] / 10, correctStance[topic" PRO"] / 10, correctOnTopic[topic" CON"] / 10, correctArgumentative[topic" CON"] / 10, correctStance[topic" CON"] / 10
  }

  if (numTopics == 0) {
    topicPrecision = 0
    argumentativePrecision = 0
    stancePrecision = 0
  } else {
    topicPrecision = correctOnTopicAll / (20 * numTopics)
    argumentativePrecision = correctArgumentativeAll / (20 * numTopics)
    stancePrecision = correctStanceAll / (20 * numTopics)
  }

  output = "'$3'"
  printf "measure {\n key: \"topicRelevanceP@10\"\n value: \"%.3f\"\n}\n", topicPrecision > output
  printf "measure {\n key: \"argumentativenessP@10\"\n value: \"%.3f\"\n}\n", argumentativePrecision > output
  printf "measure {\n key: \"stanceRelevanceP@10\"\n value: \"%.3f\"\n}\n", stancePrecision > output
}' $1 $2

