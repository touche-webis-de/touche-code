# The file Dockerfile.basis has generated webis/touche25-ad-detection:0.0.1
FROM webis/touche25-ad-detection:0.0.1

ADD predict.py models.py model_utils.py /
ADD models /models/

# We copied the source files to /
# Hence, we add / to the python path

# Ensure the tokenizer is in the docker image:
RUN python3 -c 'from transformers import AutoTokenizer; AutoTokenizer.from_pretrained(f"sentence-transformers/all-MiniLM-L6-v2")'

ENV PYTHONPATH=/

ENTRYPOINT ["python3", "/predict.py"]
