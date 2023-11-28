FROM python:3.11
# Example for PyTorch:
# FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

ENV PYTHONPATH=/

# Install requirements
COPY requirements.txt /
RUN pip3 install -r requirements.txt

ENV PYDEVD_DISABLE_FILE_VALIDATION=1
COPY random_baseline.ipynb /
RUN jupyter trust /random_baseline.ipynb

ENTRYPOINT [ "tira-run-notebook", "--notebook", "/random_baseline.ipynb", "--input", "/dataset", "--output", "/output" ]

