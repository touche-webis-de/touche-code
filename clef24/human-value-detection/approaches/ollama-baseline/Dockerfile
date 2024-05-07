FROM python:3.11

ENV PYTHONPATH=/
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Install requirements
COPY requirements.txt /
RUN pip3 install -r requirements.txt

# Copy llm-cache.json.gzip if it exists
COPY ollama_baseline.py llm-cache.json.gzip* /

ENTRYPOINT [ "python", "/ollama_baseline.py", "/dataset", "/output" ]

