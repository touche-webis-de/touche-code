#!/bin/bash
cat /dev/stdin \
  | grep -v "^Text-ID" \
  | awk -F'\t' '{printf "%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n", $1, $2, $3+$4+$5+$6, $7+$8, $9+$10, $11+$12, $13+$14+$15+$16, $17+$18, $19+$20+$21+$22, $23+$24, $25+$26+$27+$28, $29+$30, $31+$32+$33+$34, $35+$36+$37+$38+$39+$40}' \
  | awk 'BEGIN{OFS="\t"}{for(f=3;f<=NF;f+=1){if($f>1){$f=1}};print $0}' \
  > ground-truth.tsv
