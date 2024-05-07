#!/bin/bash
threshold=0
awk 'BEGIN {
    threshold = '"$threshold"'
  }{
    if (FILENAME == "ground-truth.tsv") {
      key = $1" "$2
      for (f = 3; f <= NF; f += 1) {
        label[key" "f] = $f
      }
    } else {
      if (FNR == 1) {
        for (f = 3; f <= NF; f+= 1) {
          value[f] = $f
        }
      } else {
        key = $1" "$2
        language = gensub(/_.*/, "", 1, $1)
        if (language != "HE" && language != "TR") {
          languages[language] = 1
          type = ($1 ~ /_M_/) ? "manifesto" : "news"
          for (f = 3; f <= NF; f += 1) {
            if (label[key" "f] == 1) {
              if ($f > threshold) {
                tp[language" "type" "f] += 1
                tp[language" all "f] += 1
              } else {
                fn[language" "type" "f] += 1
                fn[language" all "f] += 1
              }
            } else {
              if ($f > threshold) {
                fp[language" "type" "f] += 1
                fp[language" all "f] += 1
              } else {
                tn[language" "type" "f] += 1
                tn[language" all "f] += 1
              }
            }
          }
        }
      }
    }
  } END {
    types["manifesto"] = 1
    types["news"] = 1
    types["all"] = 1

    printf "Type\tLanguage"
    for (f = 3; f <= NF; f += 1) {
      printf "Precision %s\tRecall %s\t", value[f], value[f]
    }
    print ""
    for (type in types) {
      for (language in languages) {
        printf "%s\t%s\t", type, language
        for (f = 3; f <= NF; f += 1) {
          key = language" "type" "f
          precision = (tp[key] + fp[key] == 0) ? 0 : tp[key] / (tp[key] + fp[key])
          recall = (tp[key] + fn[key] == 0) ? 0 : tp[key] / (tp[key] + fn[key])
          printf "\t%.2f\t%.2f", precision, recall
        }
        print ""
      }
    }
  }' ground-truth.tsv $1

