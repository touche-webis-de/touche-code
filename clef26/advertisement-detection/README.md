# Baselines

This directory contains baseline systems for the shared task on "Advertisement in Retrieval-Augmented Generation" at Touché 2026.

After installing all necessary requirements specified in the corresponding `requirements.txt` files, all baselines can be run locally using the `./predict.py` or `./block.py` script in the respective README. 

To run the `minilm-baseline` for subtask 1 and the subtaks 2 baseline, you additionally need to download the required spacy pipeline via 
```
python -m spacy download en_core_web_sm
```

## Subtask 1 - Detection
For the advertisement detection task, we provide two different baselines in `subtask-1-detection`:
- a naive bayes classifier (`naive-bayes-baseline`)
- a finetuned BERT model (`minilm-baseline`)

## Subtask 2 - Span Prediction
For the span prediction task, we provide two different baselines in `subtask-2-span-prediction`:
- a finetuned BERT model (`minilm-baseline`; same as for subtask 1). This baseline outputs spans of full sentences predicted to contain advertisements.
- a dummy baseline (`last-sents-baseline`) for quick execution (e.g. setting up the datasets on TIRA)

## Subtask 3 - Blocking
This baseline takes the simplest approach to ad blocking and removes all text marked by the spans.


# Evaluation
The [task_eval](task_eval)-directory provides scripts to evaluate your runs. 
For subtask 1, the evaluation can be handled by TIRA (see the respective READMEs); the [detection.py](task_eval/detection.py)-script is provided for reference.
