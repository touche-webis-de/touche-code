# JRC Data Conversion

```bash
python3 convert_annotations.py --input "PATH/TO/valueml.zip" --verbose
```

```bash
docker build -t valueeval24-jrc-data-conversion .
docker run -it --rm -v /PATH/TO/:/data valueeval24-jrc-data-conversion data/valueml.zip -v
```
