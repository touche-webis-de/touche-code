Human Value Detection Evaluator
===============================
Evaluator for Human Value Detection 2024 @ CLEF 2024.

Example usage:
```
docker run --rm -v /PATH/TO/DATASET/validation-english:/labels -v /PATH/TO/RUN:/run -v $PWD/output:/output webis/touche-human-value-detection-evaluator:1.0.2 --inputDataset /labels --inputRun /run --outputDataset /output
```


Development
-----------
```
docker build -t webis/touche-human-value-detection-evaluator:1.0.2 .
docker push webis/touche-human-value-detection-evaluator:1.0.2
```

In TIRA:
```
python3 /evaluator.py --inputDataset $inputDataset --inputRun $inputRun --outputDataset $outputDir
```

