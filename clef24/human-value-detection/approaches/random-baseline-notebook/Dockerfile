FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

RUN pip3 install jupyterlab runnb tira==0.0.32

# Install custom requirements
COPY requirements.txt /workspace/
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/workspace

# Uncomment the following line to include the models folder
# COPY models /workspace/models/

# Copy execution notebook
COPY random_baseline_notebook.ipynb /workspace/

RUN jupyter trust /workspace/random_baseline_notebook.ipynb
