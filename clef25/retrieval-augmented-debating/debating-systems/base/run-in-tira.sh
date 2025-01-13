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

echo "Starting retrieval system"
pushd /app
./start.sh &
popd

# see https://stackoverflow.com/a/50055449
echo "Waiting for port 8080 to become available"
max_wait_seconds=3600 # one hour
timeout $max_wait_seconds bash -c 'until printf "" 2>>/dev/null >>/dev/tcp/$0/$1; do sleep 1; done' localhost 8080
echo

echo "Starting GenIRSim"
genirsim $CONFIGURATION_FILE $PARAMETER_FILE > $OUTPUT_FILE

