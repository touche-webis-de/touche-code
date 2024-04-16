# Ollama Baseline for ValueEval'24 (Script)
Ollama baseline for the task on Human Value Detection, script version.

The baseline is intended for kickstarting your own approach. Load your models
etc. at `# SETUP` and then change `predict(text)`. If you keep everything else,
your approach can be directly dockerized, run within Docker on TIRA, and run as
a server that you can call via HTTP or deploy for everyone to use.

## Usage
If you have no access to an [Ollama](https://ollama.com/) container, you can run
your own following the [official documentation](https://hub.docker.com/r/ollama/ollama). 
The `ollama_baseline.py` assumes it runs at the default port, but host and port
can be changed using the `OLLAMA_HOST` environment variable.

Requests to the Ollama server are cached in `llm-cache.json.gzip`. If it exists,
this file is added to the Docker image when building it. Since access to Ollama
is not allowed inside TIRA, create this file while running your code locally and
then create the Docker image that you can push to TIRA. Since it then has all
responses cached, it will still execute in TIRA to demonstrate replicability.

### Local usage
```bash
# install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run
python3 ollama_baseline.py ../../toy-dataset/ output/

# view result
cat output/predictions.tsv
```

### Docker usage
```bash
# build
docker build -t valueeval24-ollama-baseline:1.0.0 .

# run
# '--add-host=host.docker.internal:host-gateway' needed on Linux for accessing Ollama docker on localhost
# use '--env OLLAMA_HOST=<http-and-host-and-ip>' to use another Ollama server
docker run --rm \
  -v $PWD/../../toy-dataset:/dataset -v $PWD/output:/output \
  --add-host=host.docker.internal:host-gateway \
  valueeval24-ollama-baseline:1.0.0

# view result
cat output/predictions.tsv
```

### Server usage
Start a server that provides the `predict`-function over HTTP:
```bash
# Either for local usage (after installation):
tira-run-inference-server --script ollama_baseline.py --port 8787

# Or for docker usage (after building):
# See the comment for '--add-host' for 'run' above
docker run --rm -it --publish 8787:8787 --entrypoint tira-run-inference-server \
  --add-host=host.docker.internal:host-gateway \
  valueeval24-ollama-baseline:1.0.0 \
  --script ollama_baseline.py --port 8787
```
Then in another shell:
```bash
curl -X POST -H "application/json" \
  -d "[\"Our nature must be protected\", \"We do not always get what we want\"]" \
  localhost:8787
```

### TIRA usage
- Follow the guide on the TIRA submission page to upload the model
- Use this for the command: `python /ollama_baseline.py $inputDataset $outputDir`

