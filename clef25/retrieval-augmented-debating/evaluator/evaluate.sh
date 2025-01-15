#!/bin/bash

cd $(dirname $0) # change into parent directory of this script

RUN_DIRECTORY=
OUTPUT_DIRECTORY=
GROUND_TRUTH_DIRECTORY=

for i in "$@"; do
  case $i in
    -r=*|--run-directory=*)
      RUN_DIRECTORY="${i#*=}"
      shift # past argument=value
      ;;
    -o=*|--output-directory=*)
      OUTPUT_DIRECTORY="${i#*=}"
      shift # past argument=value
      ;;
    -g=*|--ground-truth-directory=*)
      GROUND_TRUTH_DIRECTORY="${i#*=}"
      shift # past argument=value
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
      echo "No positional parameters allowed $i"
      exit 1
      ;;
  esac
done

genirsim-evaluate /app/touche25-rad-tira-evaluate.json $RUN_DIRECTORY/*.jsonl \
  | tee $OUTPUT_DIRECTORY/evaluation.jsonl

cat $OUTPUT_DIRECTORY/evaluation.jsonl \
  | jq -r '.userTurnsEvaluations.[] | del (.milliseconds) | to_entries[] | [.key, .value.score] | @tsv' \
  | awk -F '\t' '{
      sum[$1] += $2
      cnt[$1] += 1
    } END {
      for (key in sum) {
        printf "measure{\n  key: \"%s\"\n  value: \"%f\"\n}\n", key, sum[key] / cnt[key]
      }
    }' \
  > $OUTPUT_DIRECTORY/evaluation.prototext

