#!/bin/bash


RUN_DIRECTORY=
OUTPUT_DIRECTORY=
GROUND_TRUTH_DIRECTORY=

while [ $# -gt 0 ];do
  case $1 in
    -r|--run-directory)
      shift
      RUN_DIRECTORY="$(realpath $1)"
      shift
      ;;
    -o|--output-directory)
      shift
      OUTPUT_DIRECTORY="$(realpath $1)"
      shift
      ;;
    -g|--ground-truth-directory)
      shift
      GROUND_TRUTH_DIRECTORY="$(realpath $1)"
      shift
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      echo "No positional parameters allowed $1"
      exit 1
      ;;
  esac
done

echo RUNS: $RUN_DIRECTORY/*.jsonl
echo GROUND-TRUTH: $GROUND_TRUTH_DIRECTORY
echo OUTPUT: $OUTPUT_DIRECTORY

cd $(dirname $0) # change into parent directory of this script
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

