#!/bin/bash
ls data | grep -v "^HE_" | awk '{print $1" "$1}' > tasks.txt
