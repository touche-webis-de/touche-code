# The file Dockerfile.basis has generated webis/touche25-ad-detection:0.0.1
FROM webis/touche25-ad-detection:0.0.1

ADD predict.py model.py model_utils.py models /

ENTRYPOINT ["python3", "./predict.py"]
