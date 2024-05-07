#!/bin/bash
rm sentences-translated-tmp.tsv
for text_id in $(ls data);do
  echo $text_id
  cat data/$text_id/response.json \
    | jq -r '.translations
        | to_entries[]
        | ["'"$text_id"'" ,.key+1, .value.text]
        | @tsv' \
    >> sentences-translated-tmp.tsv
done

python << END
import pandas
rows = []
with open("sentences-translated-tmp.tsv") as input_file:
  for line in input_file:
    row = line.split("\t")
    rows.append({"Text-ID":row[0], "Sentence-ID":row[1], "Text":row[2].rstrip()})
frame = pandas.DataFrame(rows)
frame.to_csv("sentences-translated.tsv", encoding="utf-8", sep="\t", index=False)
END
