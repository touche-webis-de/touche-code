ARG BASE_IMAGE_VERSION=0.3.2

FROM ghcr.io/touche-webis-de/touche25-retrieval-augmented-debating-base:${BASE_IMAGE_VERSION}-py3.13

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py start.sh ./

