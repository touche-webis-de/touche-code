#!/bin/bash

input=$1
curl -X POST 'https://api-free.deepl.com/v2/translate' \
  --header 'Authorization: DeepL-Auth-Key e9bdb3dc-0499-4a36-8889-3263d0afd41a:fx' \
  --header 'Content-Type: application/json' \
  --data "@$input"
