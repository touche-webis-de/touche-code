ARG CUDA=nocuda
FROM anibali/pytorch:1.10.2-${CUDA}-ubuntu20.04

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy download and interface module
RUN mkdir /app/components/
RUN echo > /app/components/__init__.py
# COPY components/__init__.py /app/components/__init__.py
COPY components/interface_modules /app/components/interface_modules

# download pretrained data for models
RUN mkdir /app/checkpoints
COPY checkpoints/model_sources.txt /app/checkpoints/model_sources.txt
RUN python3 -m components.interface_modules.download_pretrained_models /app/checkpoints/model_sources.txt

# copy model scripts
COPY components/toolbox /app/components/toolbox
COPY components/models /app/components/models
COPY components/data_modules /app/components/data_modules

# copy server scripts
COPY components/core /app/components/core
COPY server.py /app/server.py

# create entrypoint
CMD ["8001"]
ENTRYPOINT ["python3", "/app/server.py"]
