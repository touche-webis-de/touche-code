FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

RUN pip3 install pandas jupyterlab runnb tira==0.0.28

# Install custom requirements HERE
COPY requirements.txt /workspace/
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/workspace

# copy download and interface module
RUN mkdir /workspace/components/
RUN echo > /workspace/components/__init__.py
# COPY components/__init__.py /workspace/components/__init__.py
COPY components/interface_modules /workspace/components/interface_modules

# download pretrained data for models
RUN mkdir /workspace/checkpoints
COPY checkpoints/model_sources.txt /workspace/checkpoints/model_sources.txt
RUN python3 -m components.interface_modules.download_pretrained_models /workspace/checkpoints/model_sources.txt

# copy unzipped human_value_trained_models
RUN mkdir -p /workspace/checkpoints/human_value_trained_models/
COPY checkpoints/human_value_trained_models/*.pkl /workspace/checkpoints/human_value_trained_models/
COPY checkpoints/human_value_trained_models/HCV-409-*.ckpt /workspace/checkpoints/human_value_trained_models/
COPY checkpoints/human_value_trained_models/HCV-408-*.ckpt /workspace/checkpoints/human_value_trained_models/
COPY checkpoints/human_value_trained_models/HCV-406-*.ckpt /workspace/checkpoints/human_value_trained_models/
#COPY checkpoints/human_value_trained_models/ /workspace/checkpoints/human_value_trained_models/
# ADD ADDITIONAL CHECKPOINT FILES HERE

# copy model scripts
COPY components/toolbox /workspace/components/toolbox
COPY components/models /workspace/components/models
COPY components/data_modules /workspace/components/data_modules

# Copy execution notebook
COPY adam_smith_notebook.ipynb /workspace/

RUN jupyter trust /workspace/adam_smith_notebook.ipynb
