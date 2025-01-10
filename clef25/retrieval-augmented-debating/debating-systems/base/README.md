# Base Image for Debating Systems for Retrieval-Augmented Debating 2025

Build your image FROM this image. Add all your parts in `/app`. Add a shell script `/app/start.sh` that runs your server on port 8080.

## Entrypoints
- `/app/start.sh` (default): Script that starts your debating system on port 8080
- `/genirsim/serve.sh`: Starts the GenIRSim web application (like [genirsim.webis.de](https://genirsim.webis.de/)) on port 8000 with access to your debating system on `http://localhost:8080`
- `/genirsim/run-in-tira.sh --configuration-file=<FILE> --parameter-file=<FILE> --output-file=<FILE>`: Use this line as command in TIRA

