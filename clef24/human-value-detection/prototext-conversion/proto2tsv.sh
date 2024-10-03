#!/bin/bash

if [ $# -ne 5 ];then
  echo "Usage: <team> <dataset> <software> <run-id> <evaluation.prototext>"
fi

team=$1
dataset=$2
software=$3
runId=$4
proto=$5

cat $proto \
  | sed 's/ (Subtask 1)//' \
  | sed 's/ (Subtask 2 - overall)/ (Subtask 2)/' \
  | sed 's/ (Subtask 2 - attained)/ attained/' \
  | sed 's/ attained/ (Subtask 2 - attained)/' \
  | sed 's/ (Subtask 2 - constrained)/ constrained/' \
  | sed 's/ constrained/ (Subtask 2 - constrained)/' \
  | awk -F'"' '$1 ~ /key:/ {
        key = $2
      } $1 ~ /value:/ {
        results[key] = $2
      } END {
        metrics[1] = "F1"
        metrics[2] = "Precision"
        metrics[3] = "Recall"

        tasks[1] = ""
        tasks[2] = " (Subtask 2)"
        tasks[3] = " (Subtask 2 - attained)"
        tasks[4] = " (Subtask 2 - constrained)"

        values[1]  = ""
        values[2]  = " Self-direction: thought"
        values[3]  = " Self-direction: action"
        values[4]  = " Stimulation"
        values[5]  = " Hedonism"
        values[6]  = " Achievement"
        values[7]  = " Power: dominance"
        values[8]  = " Power: resources"
        values[9]  = " Face"
        values[10] = " Security: personal"
        values[11] = " Security: societal"
        values[12] = " Tradition"
        values[13] = " Conformity: rules"
        values[14] = " Conformity: interpersonal"
        values[15] = " Humility"
        values[16] = " Benevolence: caring"
        values[17] = " Benevolence: dependability"
        values[18] = " Universalism: concern"
        values[19] = " Universalism: nature"
        values[20] = " Universalism: tolerance"

        cnt = 1
        printf "Team\tDataset\tSoftware\tRun ID"
        for (t = 1; t <= 4; t += 1) {
          for (m = 1; m <= 3; m += 1) {
            for (v = 1; v <= 20; v += 1) {
              key = metrics[m]""values[v]""tasks[t]
              printf "\t%s", key
              if (t == 1) { printf " (Subtask 1)" }
              if (!(key in results)) {
                print "UNKNOWN KEY \""key"\""
              }
              scores[cnt] = results[key]
              cnt += 1
            }
          }
        }
        print ""

        printf "%s\t%s\t%s\t%s", "'"$team"'", "'"$dataset"'", "'"$software"'", "'"$runId"'"
        for (c = 1; c <= cnt; c += 1) {
          printf "\t%.2f", scores[c]
        }
        print ""
      }'

