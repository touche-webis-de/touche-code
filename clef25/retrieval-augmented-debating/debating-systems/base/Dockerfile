ARG BASE_IMAGE=ubuntu:24.04

FROM ${BASE_IMAGE}
ARG NVM_VERSION=0.40.1
ARG NODE_VERSION=23.6.0
ARG GENIRSIM_VERSION=0.5.3
EXPOSE 8080

# install node
RUN apt-get update && apt-get install -y \
  curl
ENV NVM_DIR /usr/local/nvm
RUN mkdir -p $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install v$NODE_VERSION && nvm use --delete-prefix v$NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin
ENV PATH $NODE_PATH:$PATH

# install GenIRSim
WORKDIR /genirsim
RUN npm install @webis-de/gen-ir-sim@${GENIRSIM_VERSION}
ENV PATH /genirsim/node_modules/.bin:$NODE_PATH:$PATH
COPY run-in-tira.sh .

# prepare for app
WORKDIR /app
ENTRYPOINT [ "/app/start.sh" ]

