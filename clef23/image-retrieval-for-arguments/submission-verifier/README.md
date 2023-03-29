Submission Verifier
===================
Verifier for "Image Retrieval for Arguments".

Development
-----------
```
docker build -t webis/touche-image-retrieval-for-arguments-submission-verifier:0.1.0 .
docker push webis/touche-image-retrieval-for-arguments-submission-verifier:0.1.0
```

In TIRA:
```
/bin/sh /submission-verifier.sh $inputDataset $inputRun $outputDir
```

