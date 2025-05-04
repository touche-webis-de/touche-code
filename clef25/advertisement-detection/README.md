# Baselines

This directory contains baseline systems for the generation of texts with and without advertisements for a given query (subtask 1), as well as for the classification of a given text, deciding whether it contains an advertisement or not (subtask 2).

After installing all necessary requirements specified in the corresponding `requirements.txt` files, all baselines can be run locally using the `./predict.py` command in the respective README. 

To run the `minilm-baseline` for subtask 2, you additionally need to download the required spacy pipeline via `python -m spacy download en_core_web_sm`.

## Subtask 1 - Generation
A simple rule-based generation approach can be found in `subtask-1-generation`.

## Subtask 2 - Detection
For the advertisement detection task, we provide two different baselines in `subtask-2-classification`:
- a naive bayes classifier (`naive-bayes-baseline`)
- a finetuned BERT model (`minilm-baseline`)

