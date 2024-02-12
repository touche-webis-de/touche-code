#!/bin/bash
#input=$1
#input_dir=$(dirname $(readlink -f $input))

#docker build -t valueeval24-inception-data-conversion .
#docker run -it --rm -v $input_dir/:/data valueeval24-inception-data-conversion data/$(basename $input)
#cp $input_dir/{labels-ground_truth.tsv,sentences.tsv} .

function get_text_ids() {
  cat labels-ground_truth.tsv \
    | awk -F '\t' '{
        for(f=3;f<=NF;f+=1) {
          values[$1]+=$f
        }
      } END {
        for (text in values) {
          printf "%s\t%d\n", text, values[text]
        }
      }' \
    | awk '$2 > 1 {print $1}'
}

get_text_ids \
  | awk -F '\t' 'BEGIN {
      split_quota["validation"] = 0.2
      split_quota["test"] = 0.2
    } {
      part = $1
      gsub(/_[^_]*$/, "", part)
      if (FILENAME == "splits.tsv") {
        assigned[part" "$2] += 1
      } else {
        totals[part] += 1
      }
    } END {
      for (part in totals) {
        for (splitt in split_quota) {
          missing = split_quota[splitt] * totals[part] - assigned[part" "splitt]
          if (missing < 0) { missing = 0 }
          printf "%s\t%s\t%d\n", part, splitt, missing
        }
      }
    }' splits.tsv /dev/stdin \
  | sort \
  > missing.tsv

get_text_ids \
  | shuf \
  | awk -F '\t' '{
      if (FILENAME == "splits.tsv") {
        part = $1
        gsub(/_[^_]*$/, "", part)
        printf "%s\t%s\n", $1, $2
        assigned[$1] = 1
      } else if (FILENAME == "missing.tsv") {
        missing[$1" "$2] = $3
      } else {
        if (!($1 in assigned)) {
          part = $1
          gsub(/_[^_]*$/, "", part)
          if (missing[part" test"] > 0) {
            missing[part" test"] -= 1
            printf "%s\t%s\n", $1, "test"
          } else if (missing[part" validation"] > 0) {
            missing[part" validation"] -= 1
            printf "%s\t%s\n", $1, "validation"
          } else {
            printf "%s\t%s\n", $1, "training"
          }
        }
      }
    }' splits.tsv missing.tsv /dev/stdin \
  | sort \
  | sponge splits.tsv

echo "Splits size:"
cat splits.tsv | sed 's/_[0-9][0-9]*//' | sort | uniq -c

rm -rf output
for split in training validation test;do
  mkdir -p output/$split
  head -n 1 sentences.tsv > output/$split/sentences.tsv
  head -n 1 labels-ground_truth.tsv > output/$split/labels.tsv
done

awk -F '\t' '{
    if (FILENAME == "splits.tsv") {
      assigned[$1] = $2
    } else if (FILENAME == "sentences.tsv") {
      if ($1 in assigned) {
        print $0 >> "output/"assigned[$1]"/sentences.tsv"
      }
    } else {
      if ($1 in assigned) {
        print $0 >> "output/"assigned[$1]"/labels.tsv"
      }
    }
  }' splits.tsv sentences.tsv labels-ground_truth.tsv

