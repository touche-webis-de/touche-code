# Inception Data Conversion

```bash
python3 convert_curation.py --input "PATH/TO/valueml.zip"
```

```bash
docker build -t valueeval24-inception-data-conversion .
docker run -it --rm -v /PATH/TO/:/data valueeval24-inception-data-conversion data/valueml.zip
```
