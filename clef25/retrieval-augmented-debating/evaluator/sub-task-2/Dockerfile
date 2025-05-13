FROM python:3.13-slim
RUN pip install "pydantic"

COPY evaluate.py /

ENTRYPOINT [ "python3", "/evaluate.py" ]
