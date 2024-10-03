VALUE RADAR PLOT
================
Make a radar plot with scores for all 19 value categories for Human Value Detection 2024 @ Touche (ValueEval'24).

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
<name>	<color>	<score-for-self-direction-thought>	<score-for-self-direction-action>	...
```
Where
- `<name>` is the name for the legend (or empty if the line should not be part of the legend)
- `<color>` is a color as recognized by R, like `blue` or `#0000FF` or `#0000FF88` (the last one is half-transparent)
- `<score-for-...>` is either `-` or a value between 0 and 1

See the [example.tsv](example-data/example.tsv) for reference.

