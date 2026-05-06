# docker build -t touche-webis-de/span-prediction-evaluator:clef26 .
FROM python:3.11-slim

WORKDIR /app

RUN pip install pandas tqdm

COPY evaluation.py /app/evaluation.py

ENTRYPOINT ["python", "/app/evaluation.py"]