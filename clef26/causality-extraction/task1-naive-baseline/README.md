# Naive Baseline For Causality Extraction Task 1 @ Touché 2026

This baseline implementation always predicts the same label. You can use it as a starting point for developing your TIRA submission. Simply edit `predict.py` to assign `df['label']` class predictions from your approach.


## Submit to TIRA

Detailed information on how to submit software to TIRA is available in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission).

To submit this baseline to TIRA, please first ensure that your TIRA client is authenticated (you can find your authentication token at [tira.io/task-overview/causality-extraction-toucheclef26](https://www.tira.io/task-overview/causality-extraction-toucheclef26/task1-spot-check-dataset-20260430-training) by clicking on `SUBMIT`):

```
tira-cli login --token YOUR-AUTHENTICATION-TOKEN
```

Next, please verify that your system has all required dependencies for a software submission to TIRA:

```
tira-cli verify-installation
```

Finally, you can upload your code submission via (add the `--dry-run` flag to test that everything works):

```
tira-cli code-submission --path . --task causality-extraction-toucheclef26 --dataset task1-spot-check-dataset-20260430-training --dry-run --command '/predict.py --dataset $inputDataset --output $outputDir'
```