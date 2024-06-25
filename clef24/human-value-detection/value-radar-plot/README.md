VALUE RADAR PLOT
================
Make a radar plot with scores for all 20 value categories for Human Value Detection 2023 @ Touche and SemEval 2023.

Setup
-----
```
Rscript -e 'install.packages(c("fmsb", "plotrix"))'
```

Usage
-----
```
./plot-values-radar.R  example-data/example.tsv example-values-radar.pdf
```

File format of input file (tab-separated):
```
<color>	<score-for-self-direction-thought>	<score-for-self-direction-action>	...
```
Where
- `<color>` is a color as recognized by R, like `blue` or `#0000FF` or `#0000FF88` (the last one is half-transparent)
- `<score-for-...>` is either `-` or a value between 0 and 1

See the [example.tsv](example-data/example.tsv) for reference.

