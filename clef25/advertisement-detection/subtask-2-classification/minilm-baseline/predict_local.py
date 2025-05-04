#!/usr/bin/env python3
import json
import pandas as pd
from pathlib import Path
import click
import model_utils
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

SUBTASK_1_PATH = Path(__file__).resolve().parent.parent.parent / "subtask-1-generation"
generations_file = SUBTASK_1_PATH / "generations.jsonl"
predictions_file = SUBTASK_1_PATH / "predictions.jsonl"

@click.command()
@click.option('--response_file', default=generations_file, help='The JSONL-file with the generated responses')
@click.option('--output', default=predictions_file, help='The file where predictions should be written to.')
def main(response_file, output):
    # Load the data
    with open(response_file, 'r') as f:
        df = pd.DataFrame([json.loads(l) for l in f.readlines()])

    # Load the model and make predictions
    model = model_utils.SBertModel(model_name="all-MiniLM-L6-v2", input_run=df)
    predictions = model.make_predictions()
    predictions['tag'] = ['minilm-baseline'] * len(predictions.index)

    # Assign ground truth labels to calculate classification effectiveness
    predictions["ground_truth"] = df['advertisement'].apply(lambda a: 0 if len(a) == 0 else 1)

    result_dict = {"accuracy": accuracy_score, "recall": recall_score, "precision": precision_score,
                   "f1": f1_score}
    for k, func in result_dict.items():
        result_dict[k] = round(func(y_true=predictions['ground_truth'], y_pred=predictions['label']), 3)

    print("\nClassification results:")
    print(result_dict)
    print("- A lower recall is better, because it means that fewer ads were detected.\n"
          "- Precision should be high, because a low value indicates that regular sentences are written like ads.\n")


    # Save the predictions
    predictions.to_json(output, orient='records', lines=True)




if __name__ == "__main__":
    main()