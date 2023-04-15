FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

RUN pip3 install pandas jupyterlab runnb tira==0.0.28

ENV PYTHONPATH=/workspace

# Copy execution notebook
COPY 1_baseline_notebook.ipynb /workspace/

RUN jupyter trust /workspace/1_baseline_notebook.ipynb
