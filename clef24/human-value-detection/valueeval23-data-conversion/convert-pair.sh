#!/bin/bash

if [ $# -lt 2 ];then
  echo "Usage: $0 <arguments-file> <labels-file> [<output-prefix>]" > /dev/stderr
  exit 1
fi

output_sentences=$3sentences.tsv
output_labels=$3labels.tsv

echo -e "Text-ID\tSentence-ID\tText" > $output_sentences
echo -e "Text-ID\tSentence-ID\tSelf-direction: thought attained\tSelf-direction: thought constrained\tSelf-direction: action attained\tSelf-direction: action constrained\tStimulation attained\tStimulation constrained\tHedonism attained\tHedonism constrained\tAchievement attained\tAchievement constrained\tPower: dominance attained\tPower: dominance constrained\tPower: resources attained\tPower: resources constrained\tFace attained\tFace constrained\tSecurity: personal attained\tSecurity: personal constrained\tSecurity: societal attained\tSecurity: societal constrained\tTradition attained\tTradition constrained\tConformity: rules attained\tConformity: rules constrained\tConformity: interpersonal attained\tConformity: interpersonal constrained\tHumility attained\tHumility constrained\tBenevolence: caring attained\tBenevolence: caring constrained\tBenevolence: dependability attained\tBenevolence: dependability constrained\tUniversalism: concern attained\tUniversalism: concern constrained\tUniversalism: nature attained\tUniversalism: nature constrained\tUniversalism: tolerance attained\tUniversalism: tolerance constrained" > $output_labels


cat $1 \
  | awk -F"\t" 'BEGIN {
        output_sentences = "sort -k 1,1 -k 2,2n  >> '$output_sentences'"
        output_labels = "sort -k 1,1 -k 2,2n >> '$output_labels'"
      } FNR > 1 {
        if (FILENAME == "/dev/stdin") {
          if ($2 in text_ids) {
            sentence_ids[$2] += 1
          } else {
            text_ids[$2] = $1
            sentence_ids[$2] = 1
          }
          printf "%s\t%s\t%s\n", text_ids[$2], sentence_ids[$2], $4 | output_sentences
          text_id_for_arg_id[$1] = text_ids[$2]
          sentence_id_for_arg_id[$1] = sentence_ids[$2]
          stance_for_arg_id[$1] = $3
        } else {
          printf "%s\t%s", text_id_for_arg_id[$1], sentence_id_for_arg_id[$1] | output_labels
          for (f = 2; f < NF; f += 1) {
            if (stance_for_arg_id[$1] == "against") {
              printf "\t0\t%s", $f | output_labels
            } else {
              printf "\t%s\t0", $f | output_labels
            }
          }
          printf "\n" | output_labels
        }
      }' /dev/stdin $2
