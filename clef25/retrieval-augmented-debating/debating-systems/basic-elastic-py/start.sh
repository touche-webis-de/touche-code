#!/bin/bash

cd $(dirname $0) # change into parent directory of this script
fastapi run --port 8080 main.py

