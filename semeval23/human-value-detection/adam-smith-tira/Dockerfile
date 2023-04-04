FROM tira/submission-base-image:1.0.0

COPY requirements.txt /workspace/
RUN pip3 install -r requirements.txt

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
COPY checkpoints/human_value_trained_models/HCV-409-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt /workspace/checkpoints/human_value_trained_models/
# ADD ADDITIONAL CHECKPOINT FILES HERE

# copy model scripts
COPY components/toolbox /workspace/components/toolbox
COPY components/models /workspace/components/models
COPY components/data_modules /workspace/components/data_modules

COPY adam_smith_notebook.ipynb /workspace/

RUN jupyter trust /workspace/adam_smith_notebook.ipynb
