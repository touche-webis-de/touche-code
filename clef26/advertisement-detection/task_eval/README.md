## README: Evaluating Local Runs

This repository provides evaluation scripts for:

* Subtask 1: Ad Detection (`detection.py`)
* Subtask 2: Span Prediction (`span_prediction.py`)
* Subtask 3: Blocking (`blocking_manual.py` and `blocking_llm.py`)

### General Setup

* Install dependencies via the [requirements.txt](requirements.txt).
* Prepare:

  * A **run file** (`.jsonl`) containing your predictions
  * Optionally, a **truth file** (`.jsonl`). If not provided, the script attempts to load it via TIRA based on the dataset.

---

## 1. Ad Detection (`detection.py`)

### Running the Evaluation

```bash
python detection.py <dataset> --run_file path/to/predictions.jsonl --truth_file path/to/truth.jsonl
```

* `dataset`: Name of the dataset (used for organizing outputs)
* `--run_file`: Path to your predictions
* `--truth_file`: Optional; if omitted, TIRA is used

### Metrics

The evaluator computes:

* Precision
* Recall
* F1-score

### Output

Results are saved to: `evaluation/<dataset>/<stem of the run_file>/scores.json`

---

## 2. Span Prediction (`span_prediction.py`)

### Running the Evaluation

```bash
python span_prediction.py <dataset> --run_file path/to/predictions.jsonl --truth_file path/to/truth.jsonl
```

* `dataset`: Name of the dataset (used for organizing outputs)
* `--run_file`: Path to your predictions
* `--truth_file`: Optional; if omitted, TIRA is used

### Evaluation Process

* Each response is evaluated independently
* Metrics are computed per response, then averaged (macro average)

### Metrics

Per response:

* Precision
* Recall
* F1
* Granularity (penalizes over-segmentation)
* F1 with granularity penalty (`f1_gran`)
* Intersection over Union (IoU)

### Output

* Per-response results:

  * `evaluation/<dataset>/<stem of the run_file>/element_scores.jsonl`
* Aggregated results:

  * `evaluation/<dataset>/<stem of the run_file>/scores.json`

---

## Blocking
The submissions for the blocking task can be evaluated in one of two ways:

1. Manual (`blocking_manual.py`)
2. With an LLM (`blocking_llm.py`); Requires an env variable `OPENAI_API_KEY`

### Metrics

Both evaluators compute:

* Correctness
* Fluency
* Relevance

### Running the Evaluation (Manual)

```bash
streamlit run blocking_manual.py -- <dataset> --run_file path/to/generations.jsonl --truth_file path/to/truth.jsonl
```

* `dataset`: Name of the dataset (used for organizing outputs)
* `--run_file`: Path to your predictions
* `--truth_file`: Optional; if omitted, TIRA is used

### Running the Evaluation (LLM)

```bash
python blocking_llm.py <dataset> --run_file path/to/generations.jsonl --truth_file path/to/truth.jsonl
```

* `dataset`: Name of the dataset (used for organizing outputs)
* `--run_file`: Path to your predictions
* `--truth_file`: Optional; if omitted, TIRA is used

### Output

Results are saved to: 

1. `evaluation/<dataset>/<stem of the run_file>/scores_manual.json`
2. `evaluation/<dataset>/<stem of the run_file>/scores_llm.json`