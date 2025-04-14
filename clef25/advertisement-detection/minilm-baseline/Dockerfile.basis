#docker build -t webis/touche25-ad-detection:0.0.1 -f Dockerfile.basis .
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

COPY requirements.txt .

RUN pip3 install -r ./requirements.txt \
	&& apt-get update

RUN python3 -m spacy download "en_core_web_sm"
