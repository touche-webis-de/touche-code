#!/bin/bash

CONFIGURATION_FILE=
PARAMETER_FILE=
OUTPUT_FILE=/dev/stdout

for i in "$@"; do
  case $i in
    -c=*|--configuration-file=*)
      CONFIGURATION_FILE="${i#*=}"
      shift # past argument=value
      ;;
    -p=*|--parameter-file=*)
      PARAMETER_FILE="${i#*=}"
      shift # past argument=value
      ;;
    -o=*|--output-file=*)
      OUTPUT_FILE="${i#*=}"
      shift # past argument=value
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
      echo "No positional parameters allowed $i"
      exit 1
      ;;
  esac
done

if [ "$CONFIGURATION_FILE" == "" ];then
  echo "Missing option --configuration-file=<FILE>"
  exit 2
fi

# start /app/start.sh and wait for 8080 to become available

genirsim $CONFIGURATION_FILE $PARAMETER_FILE > $OUTPUT_FILE

