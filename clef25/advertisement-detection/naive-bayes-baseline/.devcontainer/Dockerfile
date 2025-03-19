# docker build -t webis/advertisement-detection-naive-bayes:0.0.1-dev .
FROM continuumio/miniconda3

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y git curl wget gcc zip unzip
RUN pip3 install pandas 'git+https://github.com/tira-io/tira.git@main#egg=tira&subdirectory=python-client' scikit-learn click
