ARG BASE_IMAGE=ubuntu:24.04

FROM ${BASE_IMAGE}
ARG NVM_VERSION=0.40.1
ARG NODE_VERSION=23.6.0
ARG GENIRSIM_VERSION=0.9.0

# App
EXPOSE 8080
# GenIRSim server
EXPOSE 8000

# install node
RUN apt-get update && apt-get install -y \
  unzip \
  wget
ENV NVM_DIR=/usr/local/nvm
RUN mkdir -p $NVM_DIR
RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install v$NODE_VERSION && nvm use --delete-prefix v$NODE_VERSION"
ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin
ENV PATH=$NODE_PATH:$PATH

# install GenIRSim
WORKDIR /genirsim
RUN npm install @webis-de/gen-ir-sim@${GENIRSIM_VERSION}
ENV PATH=/genirsim/node_modules/.bin:$NODE_PATH:$PATH
RUN wget https://github.com/webis-de/GenIRSim/archive/refs/tags/v${GENIRSIM_VERSION}.zip \
  && unzip v${GENIRSIM_VERSION}.zip "GenIRSim-${GENIRSIM_VERSION}/static/*" \
  && mv GenIRSim-${GENIRSIM_VERSION}/static . \
  && rm -r v${GENIRSIM_VERSION}.zip GenIRSim-${GENIRSIM_VERSION}
COPY run.sh serve.sh touche25-rad-tira.json ./

# prepare for app
WORKDIR /app
ENTRYPOINT [ "/app/start.sh" ]

