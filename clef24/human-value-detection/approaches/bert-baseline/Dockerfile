#FROM python:3.11
# Example for PyTorch:
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

ENV PYTHONPATH=/

# Install requirements
WORKDIR /
COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY bert_baseline.py /

ENTRYPOINT [ "python", "/bert_baseline.py", "/dataset", "/output" ]

