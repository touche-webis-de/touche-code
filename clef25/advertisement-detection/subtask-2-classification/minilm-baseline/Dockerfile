# The file .devcontainer/Dockerfile has generated webis/touche25-ad-detection:0.0.1
FROM webis/touche25-ad-detection:0.0.1

ADD predict.py models.py model_utils.py /
ADD models /models/

# We copied the source files to /
# Hence, we add / to the python path

# Ensure the tokenizer is in the docker image:
RUN python3 -c 'from transformers import AutoTokenizer, AutoModel; AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2"); AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2");'

ENV PYTHONPATH=/

ENTRYPOINT ["python3", "/predict.py"]
