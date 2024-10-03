# JRC Data Conversion

## Commands

```bash
python3 convert_annotations.py -i "PATH/TO/annotations.zip" -m PATH/TO/map_author_anonid.json -v
```

```bash
docker build -t valueeval24-jrc-data-conversion .
docker run -it --rm -v /PATH/TO/:/data valueeval24-jrc-data-conversion -i data/annotations.zip -m data/map_author_anonid.json -v
```

## Data Format

`texts.tsv`:
- `Text-ID`: The respective document ID
- `Segment`: The sequential numbering for each segment in the document
- `Text`: The cleaned text of the segment
- `Index`: The starting offset for `Text` i.r. to the overall cleaned document
- `Length`: The length of `Text`

`codes.tsv`:
- `Text-ID`: See above
- `Segment`: See above
- `Coder`: The anonymized coder reference
- `Coded-Text`: The annotated text of the specified segment
- `Index`: The starting offset for `Coded-Text` i.r. to the overall document
- `Length`: The length of `Coded-Text`
- `Value`: The annotated value (from the list of 19 values)
- `Coarse-Value`: The annotated value (from the coarse list of 10 values)
- `Attainment`: The specified attainment; one of `(Partially) attained`, `(Partially) constrained`, or `Not sure, can’t decide`
- `Time`: The timestamp in format `YYYY-mm-dd HH:MM:SS`