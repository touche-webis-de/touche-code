Random Baseline
===============

Example usage:
```
# get files
wget https://files.webis.de/corpora/corpora-webis/corpus-touche-image-search-23/topics.xml
wget https://files.webis.de/corpora/corpora-webis/corpus-touche-image-search-23/image-ids.txt
# run baseline
./random-baseline.sh . .
```

Development
-----------
```
docker build -t webis/touche-image-retrieval-for-arguments-random-baseline:0.1.0 .
docker push webis/touche-image-retrieval-for-arguments-random-baseline:0.1.0
```

In TIRA:
```
/bin/sh /random-baseline.sh $inputDataset $outputDir
```

