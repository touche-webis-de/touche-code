# New York Times Downloader

Code to create the `arguments-test-nyt.tsv` for the [ValueEval'23 dataset](https://doi.org/10.5281/zenodo.6814563).

Run the following commands:
```
$ pip3 install -r requirements.txt
$ spacy download en_core_web_sm
$ python3 nyt-downloader.py --input-file nyt01-spans.tsv --output-file arguments-test-nyt.tsv
$ sha256sum --check arguments-test-nyt.sha256
```

The `nyt-downloader.py` may sometimes time out (error message contains `net::ERR_TIMED_OUT`). Then the Internet Archive is likely under heavy load. Please try again later.

Code was written by [Zeljko Bekcic](https://github.com/zeljkobekcic) and slightly adapted by [Johannes Kiesel](https://github.com/johanneskiesel).
