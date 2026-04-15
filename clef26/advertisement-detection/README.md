# Baselines

This directory contains baseline systems for the shared task on "Advertisement in Retrieval-Augmented Generation" at Touché 2026.

After installing all necessary requirements specified in the corresponding `requirements.txt` files, all baselines can be run locally using the `./predict.py` command in the respective README. 

To run the `minilm-baseline` for subtask 1, you additionally need to download the required spacy pipeline via `python -m spacy download en_core_web_sm`.

## Subtask 1 - Detection
For the advertisement detection task, we provide two different baselines in `subtask-1-detection`:
- a naive bayes classifier (`naive-bayes-baseline`)
- a finetuned BERT model (`minilm-baseline`)