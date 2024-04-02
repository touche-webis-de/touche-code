#!/bin/bash
ls data | awk '{print $1" "$1}' > tasks.txt
