FROM python:3.11
# Example for PyTorch:
# FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

ENV PYTHONPATH=/

# Install requirements
COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY attained_baseline.py /

ENTRYPOINT [ "python", "/attained_baseline.py", "/dataset", "/output" ]

