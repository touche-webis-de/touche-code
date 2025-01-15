# Base Image for Debating Systems for Retrieval-Augmented Debating 2025

Build your image FROM this image. Add your code in `/app`. Add an executable shell script `/app/start.sh` to the image that runs your server on port 8080.

Examples:
  - [Basic Elastic System (JavaScript)](../basic-elastic-js/)


## API
Your server (started through `/app/start.sh`) has to consume a JSON object that has at least the property messages, which is an array of message objects. Each message object has the string property `role`, which is either `"assistant"` or `"user"`, and the string property `content` that contains the message text.

Your server has to produce a JSON object that has at least the properties `content`, which is the text of the response message, and `arguments`, which is a list of objects corresponding to the arguments from our collection that the response is based on and that have at least the property `id`, which is the ID of the respective argument in our collection.

Example:
```
# Start our Basic Elastic System example; use CTRL-C to stop it after use
docker run --rm -it -p 127.0.0.1:8080:8080 ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-basic-elastic-js:latest

# Request the API in a different terminal
curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d '{
  "messages": [
    {"role":"user","content":"I think that it is always wrong to lie since the ten commandments tell us so."},
    {"role":"assistant","content":"I actually think theres a strong case to be made for the idea that \"There is nothing inherently morally wrong about lying.\" In certain situations, like protecting someones life or preventing harm, lying might be seen as a morally justifiable action."},
    {"role":"user","content":"But \"preventing harm\" is a slippery slope."}
  ]
}'
```
Response:
```
{
  "content":"The \"slippery slope\" is not always a fallacy.",
  "arguments": [
    { "id": "TODO" }
  ]
}
```



## Entrypoints
All Docker images build FROM this image have the following entrypoints (specified on `docker run` via `--entrypoint`):
- `/app/start.sh` (default): Script that starts your debating system on port 8080. When run as a Docker container, use `--publish 127.0.0.1:8080:8080` to have your system available at [localhost:8080](http://localhost:8080).
- `/genirsim/serve.sh`: Starts the [GenIRSim](https://github.com/webis-de/GenIRSim) web application (like [genirsim.webis.de](https://genirsim.webis.de/)) on port 8000 with access to your debating system on `http://localhost:8080`. All paramters are passed to the `/app/start.sh`. When run as a Docker container, use `--publish 127.0.0.1:8000:8000` to have the web application available at [localhost:8000](http://localhost:8000).
- `/genirsim/run.sh`: Runs [GenIRSim](https://github.com/webis-de/GenIRSim) with the specified configuration and parameter file. When run as a Docker container, use `--volume` to make your local files available inside docker.
  - `--configuration-file=<FILE>`: The GenIRSim configuration file. Default: [touche25-rad-tira.json](touche25-rad-tira.json).
  - `--parameter-file=<FILE>`: If the configuration file has parameters placeholders (`{{PARAMETER_NAME}}`, like the default one), this tab-separated-values file specifies the parameter values. The first line (header) contains the parameter names and each other line corresponds to one simulation run, with the values in each column replacing the respective parameter placeholders in the configuration.
  - `--output-file=<FILE>`: JSONL file with each line corresponding to a JSON output for the GenIRSim run.
  - `--`: Everything after this parameter is passed to the `/app/start.sh`.


## Development
The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-base) when a tag matching `rad25-base-v*` is pushed.
```
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "rad25-base-v$version"
git push origin "rad25-base-v$version"
```

