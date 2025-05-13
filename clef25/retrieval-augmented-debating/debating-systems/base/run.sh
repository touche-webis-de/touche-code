#!/bin/bash

CONFIGURATION_FILE=/genirsim/touche25-rad-tira.json
EVALUATE_RUN_FILE=
PARAMETER_FILE=
OUTPUT_FILE=/dev/stdout

for i in "$@"; do
  case $i in
    -c=*|--configuration-file=*)
      CONFIGURATION_FILE="${i#*=}"
      shift # past argument=value
      ;;
    -e=*|--evaluate-run-file=*)
      EVALUATE_RUN_FILE="${i#*=}"
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
    --)
      shift # pass remaining arguments to start.sh
      break
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

echo "Starting local system: ./start.sh $@"
pushd /app
 ./start.sh $@ &
popd


# see https://stackoverflow.com/a/50055449
echo "Waiting for port 8080 to become available"
max_wait_seconds=3600 # one hour
timeout $max_wait_seconds bash -c 'until printf "" 2>>/dev/null >>/dev/tcp/$0/$1; do sleep 1; done' 127.0.0.1 8080
echo

if [ "$EVALUATE_RUN_FILE" == "" ];then
  echo "Starting GenIRSim"
  genirsim $CONFIGURATION_FILE $PARAMETER_FILE > $OUTPUT_FILE
else
  echo "Starting GenIRSim to evaluate $EVALUATE_RUN_FILE"
  genirsim-evaluate $CONFIGURATION_FILE $EVALUATE_RUN_FILE > $OUTPUT_FILE
fi
