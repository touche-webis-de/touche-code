#!/bin/bash

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
cd /genirsim
genirsim-server

