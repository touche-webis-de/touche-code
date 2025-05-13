ARG BASE_IMAGE_VERSION=0.4.0

FROM ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-base:${BASE_IMAGE_VERSION}-py3.13

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY touche25-rad-tira.json /genirsim/touche25-rad-tira.json
COPY main.py start.sh ./

