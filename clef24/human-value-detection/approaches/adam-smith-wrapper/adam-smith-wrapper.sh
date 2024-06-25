#!/bin/bash
tmpin=/tmp/input-$$
tmpout=/tmp/output-$$
mkdir -p $tmpin $tmpout

echo "Convert input"
cat $1/sentences.tsv \
  | awk -F'\t' '{
      if (NR == 1) {
        print "Argument ID\tConclusion\tStance\tPremise"
      } else {
        printf "%s\t%s\t \t \n", $1"---"$2, $3
      }
    }' \
  > $tmpin/arguments.tsv

echo "Run prediction"
python3 /app/predict.py --inputDataset $tmpin --outputDir $tmpout

echo "Convert output"

cat $tmpout/*.tsv \
  | sed 's/---/\t/' \
  | awk  -F'\t' '{
      if (NR == 1) {
        print "Text-ID\tSentence-ID\tSelf-direction: thought attained\tSelf-direction: thought constrained\tSelf-direction: action attained\tSelf-direction: action constrained\tStimulation attained\tStimulation constrained\tHedonism attained\tHedonism constrained\tAchievement attained\tAchievement constrained\tPower: dominance attained\tPower: dominance constrained\tPower: resources attained\tPower: resources constrained\tFace attained\tFace constrained\tSecurity: personal attained\tSecurity: personal constrained\tSecurity: societal attained\tSecurity: societal constrained\tTradition attained\tTradition constrained\tConformity: rules attained\tConformity: rules constrained\tConformity: interpersonal attained\tConformity: interpersonal constrained\tHumility attained\tHumility constrained\tBenevolence: caring attained\tBenevolence: caring constrained\tBenevolence: dependability attained\tBenevolence: dependability constrained\tUniversalism: concern attained\tUniversalism: concern constrained\tUniversalism: nature attained\tUniversalism: nature constrained\tUniversalism: tolerance attained\tUniversalism: tolerance constrained"
      } else {
        printf "%s\t%s", $1, $2
        for (v = 1; v <= 19; v += 1) {
          printf "\t%.2f\t0.00", $(2+v)
        }
        print ""
      }
    }' \
  > $2/predictions.tsv

