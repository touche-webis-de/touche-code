# Base Image for Debating Systems for Retrieval-Augmented Debating 2025

Build your image FROM this image. Add all your parts in `/app`. Add a shell script `/app/start.sh` that runs your server on port 8080.

## Entrypoints
- `/app/start.sh` (default): Script that starts your debating system on port 8080
- `/genirsim/serve.sh`: Starts the GenIRSim web application (like [genirsim.webis.de](https://genirsim.webis.de/)) on port 8000 with access to your debating system on `http://localhost:8080`
- `/genirsim/run-in-tira.sh --configuration-file=<FILE> --parameter-file=<FILE> --output-file=<FILE>`: Use this line as command in TIRA


## Development
The image is built automatically on [Github](https://github.com/touche-webis-de/touche-code/pkgs/container/touche25-retrieval-augmented-debating-base) when a tag matching `rad25-base-v*` is pushed.
```
# After push of changes
version=X.X.X # semantic versioning, check Github for last version
git tag "v$version"
git push origin "v$version"
```

