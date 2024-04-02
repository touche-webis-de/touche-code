#!/bin/bash
rm sentences-translated.tsv
for text_id in $(ls data);do
  echo $text_id
  cat data/$text_id/response.json \
    | jq -r '.translations
        | to_entries[]
        | ["'"$text_id"'" ,.key+1, .value.text]
        | @tsv' \
    >> sentences-translated.tsv
done
