# The file Dockerfile.basis has generated webis/touche25-ad-detection:0.0.1
FROM webis/touche25-ad-detection:0.0.1

ADD predict.py models.py model_utils.py /
ADD models /models/

# We copied the source files to /
# Hence, we add / to the python path

ENV PYTHONPATH=/

ENTRYPOINT ["python3", "/predict.py"]
