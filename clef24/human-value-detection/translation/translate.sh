#!/bin/bash

input=$1
curl -X POST 'https://api.deepl.com/v2/translate' \
  --header "Authorization: DeepL-Auth-Key $(cat deepl-api-key.txt)" \
  --header 'Content-Type: application/json' \
  --data "@$input"
