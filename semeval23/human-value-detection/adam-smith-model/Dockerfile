ARG CUDA=nocuda
FROM anibali/pytorch:1.10.2-${CUDA}-ubuntu20.04

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
USER root
COPY data_modules/ /app/data_modules
COPY models/ /app/models
COPY toolbox/ /app/toolbox

# copy & unzip human_value_trained_models.zip
RUN mkdir /app/checkpoints
COPY checkpoints/human_value_trained_models.zip /app/checkpoints/human_value_trained_models.zip
RUN python3 /app/toolbox/zip_utils.py /app/checkpoints/human_value_trained_models.zip /app/checkpoints/
RUN rm /app/checkpoints/human_value_trained_models.zip

# download pretrained data for models
COPY download_pretrained_models.py /app/download_pretrained_models.py
RUN python3 /app/download_pretrained_models.py /app/checkpoints/human_value_trained_models /app/inputDataset

COPY predict.py /app/predict.py
