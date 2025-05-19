Code for Histograms and Line Charts
===================================

Accept the usage terms and download `valueeval24.zip` from [the dataset on Zenodo](https://doi.org/10.5281/zenodo.13283288). Then unzip and run the R script on all (ground-truth) label files:

```
unzip valueeval24.zip;
Rscript analyze-dataset.R valueeval24/*-english/labels.tsv
```

(same results are produced when using not the English translations)

- Figure number of texts and sentences per language in the final dataset: `files-per-language.pdf` + `sentences-per-language.pdf`
- Figure percentage of sentences with the number of values annotated: `fraction-sentences-with-value-per-language.pdf` + `fraction-sentences-with-value-per-language-zoomed.pdf`
- Figure overall count of refined values annotations: `sentences-per-value.pdf`
- Figure frequency of basic values annotations by language group: `sentences-with-value-per-language.pdf`
- Figure fraction of sentences with a specific value for news articles and manifestos per language: `fraction-sentences-per-value-news-*.pdf` + `fraction-sentences-per-value-manifestos-*.pdf`
- Table value attainment categorization across all texts for refined and basic values: printed to console

Figures were converted to PNGs using:

```
for input in *.pdf;do convert $input -resize 1000x $(echo $input | sed 's/df$/ng/');done
```

