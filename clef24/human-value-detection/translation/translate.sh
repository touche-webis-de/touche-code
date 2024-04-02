#!/bin/bash

input=$1
curl -X POST 'https://api.deepl.com/v2/translate' \
  --header 'Authorization: DeepL-Auth-Key a9c47d7c-99ed-4b32-bccb-50b16f65d067' \
  --header 'Content-Type: application/json' \
  --data "@$input"
