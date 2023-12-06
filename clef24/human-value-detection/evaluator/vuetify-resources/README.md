
## For Development

Import the subfolder
[result-rendering-with-vue](result-rendering-with-vue)
as project into your IDE.

Create the Docker-Image for the dev-container:
```bash
docker build -f Dockerfile.vuetify -t webis-de/vuetify-dev-container:0.1 .
```

Start the dev-container by mounting the project
[result-rendering-with-vue](result-rendering-with-vue)
into the dev-containers working directory.

Note: If the node_modules are not present in your working directory after starting the dev-container you'd have to create a symlink to the already installed modules in the container.
These are located at `/workspace/node_modules/`.
