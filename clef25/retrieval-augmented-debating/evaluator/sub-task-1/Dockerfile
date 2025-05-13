ARG BASE_IMAGE_VERSION=0.2.2

FROM ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-base:${BASE_IMAGE_VERSION}

RUN apt-get update && apt-get install -y \
  jq

COPY evaluate.sh touche25-rad-tira-evaluate.json ./

ENTRYPOINT [ "/app/evaluate.sh" ]

