ARG CUDA=nocuda
FROM anibali/pytorch:1.10.2-${CUDA}-ubuntu20.04

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
USER root
COPY data_modules/ /app/data_modules
COPY models/ /app/models

# Download model files
RUN mkdir /app/checkpoints
COPY download_model_checkpoints.py /app/download_model_checkpoints.py
RUN python3 /app/download_model_checkpoints.py /app/checkpoints

COPY predict.py /app/predict.py
