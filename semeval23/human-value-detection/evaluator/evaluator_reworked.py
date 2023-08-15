#!/usr/bin/env python3

"""Evaluator for Human Value Detection 2023 @ Touche and SemEval 2023"""
# Version: 2023-08-13

import argparse
import os
from typing import Union, Dict

import pandas as pd


# level 1
# availableValues = ["Be ambitious", "Be behaving properly", "Be broadminded", "Be capable", "Be choosing own goals", "Be compliant", "Be courageous", "Be creative", "Be curious", "Be daring", "Be forgiving", "Be helpful", "Be holding religious faith", "Be honest", "Be honoring elders", "Be humble", "Be independent", "Be intellectual", "Be just", "Be logical", "Be loving", "Be neat and tidy", "Be polite", "Be protecting the environment", "Be respecting traditions", "Be responsible", "Be self-disciplined", "Have a comfortable life", "Have a good reputation", "Have an exciting life", "Have an objective view", "Have a safe country", "Have a sense of belonging", "Have a stable society", "Have a varied life", "Have a world at peace", "Have a world of beauty", "Have equality", "Have freedom of action", "Have freedom of thought", "Have good health", "Have harmony with nature", "Have influence", "Have life accepted as is", "Have loyalty towards friends", "Have no debts", "Have pleasure", "Have privacy", "Have social recognition", "Have success", "Have the own family secured", "Have the right to command", "Have the wisdom to accept others", "Have wealth"]
# level 2
availableValues = ["Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance", "Universalism: objectivity"]


def read_labels(directory: str, prefix: Union[str, None] = None, available_argument_ids=None) -> Dict[str, Dict[str, int]]:
    labels = {}
    for labels_base_name in os.listdir(directory):
        if labels_base_name.endswith(".tsv"):
            if prefix is None or labels_base_name.startswith(prefix):
                labels_file_name = os.path.join(directory, labels_base_name)
                with open(labels_file_name, "r", newline='', encoding='utf-8-sig') as labelsFile:
                    print(f"Reading {labels_file_name}")
                    labels_frame = pd.read_csv(labelsFile, header=0, index_col=None, sep='\t')
                    labels_frame.index += 1

                    col_names = labels_frame.columns

                    has_invalid_field_names = False
                    has_argument_id = False
                    for field_name in col_names:
                        if field_name == 'Argument ID':
                            has_argument_id = True
                        elif field_name not in availableValues:
                            has_invalid_field_names = True
                            print(
                                f"Skipping file {labels_file_name} due to invalid field '{field_name}'; available field names: {str(availableValues)}")
                            break
                    if not has_argument_id:
                        print(f"Skipping file {labels_file_name} due to missing field 'Argument ID'")
                        print(list(col_names))
                        continue
                    if has_invalid_field_names:
                        continue

                    for i, row in enumerate(labels_frame.to_dict('records')):
                        argumentId = row['Argument ID']
                        if available_argument_ids is not None and argumentId not in available_argument_ids:
                            print(f"Skipping line {i + 1} due to unknown Argument ID '{argumentId}'")
                            continue
                        del row['Argument ID']

                        invalid_labels = [label for label in row.values() if label not in [0, 1]]
                        if len(invalid_labels) > 0:
                            print(f"Skipping line {i + 1} due to invalid label(s) '{invalid_labels}'")
                            continue

                        labels[argumentId] = row
    if len(labels) == 0:
        raise OSError(
            "No {}labels found in directory '{}'".format(
                '' if prefix is None else f'\'{prefix}\' ',
                directory
            )
        )
    return labels


def initialize_counter() -> Dict[str, int]:
    return {value: 0 for value in availableValues}


def write_evaluation(truth_labels: Dict[str, Dict[str, int]], run_labels: Dict[str, Dict[str, int]], output_dataset: str):
    num_instances = len(truth_labels)
    print(f"Truth labels: {num_instances}\nRun labels:   {len(run_labels)}")

    if not os.path.exists(output_dataset):
        os.makedirs(output_dataset)

    relevants = initialize_counter()
    positives = initialize_counter()
    true_positives = initialize_counter()

    for argumentId, labels in truth_labels.items():
        corresponding_run_labels = run_labels.get(argumentId, None)
        for value, truth_label in labels.items():
            if truth_label == 1:
                relevants[value] += 1
                if corresponding_run_labels is not None and corresponding_run_labels[value] == 1:
                    positives[value] += 1
                    true_positives[value] += 1
            elif corresponding_run_labels is not None and corresponding_run_labels[value] == 1:
                positives[value] += 1

    precisions: Dict[str, float] = {
        value: 0 if positives[value] == 0 else true_positives[value] / positives[value]
        for value in availableValues if relevants[value] != 0
    }
    recalls: Dict[str, float] = {
        value: true_positives[value] / relevants[value]
        for value in availableValues if relevants[value] != 0
    }
    f1_scores: Dict[str, float] = {
        value: 0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
        for (value, precision), recall in zip(precisions.items(), recalls.values())
    }

    precision = sum(precisions.values()) / len(precisions)
    recall = sum(recalls.values()) / len(recalls)
    f1_score = 2 * precision * recall / (precision + recall)

    with open(os.path.join(output_dataset, "evaluation.prototext"), "w") as evaluationFile:
        evaluationFile.write(
            f'measure{{\n key: "Precision"\n value: "{precision}"\n}}\n'
            f'measure{{\n key: "Recall"\n value: "{recall}"\n}}\n'
            f'measure{{\n key: "F1"\n value: "{f1_score}"\n}}\n'
        )

        for value in availableValues:
            if value in precisions.keys():
                evaluationFile.write(
                    f'measure{{\n key: "Precision {value}"\n value: "{precisions[value]}"\n}}\n'
                    f'measure{{\n key: "Recall {value}"\n value: "{recalls[value]}"\n}}\n'
                    f'measure{{\n key: "F1 {value}"\n value: "{f1_scores[value]}"\n}}\n'
                )


def parse_args():
    arser = argparse.ArgumentParser(
        description="Evaluator for Human Value Detection 2023 @ Touche and SemEval 2023")
    arser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least the 'labels-*.tsv'")
    arser.add_argument(
        "-r", "--inputRun", type=str, required=True,
        help="Directory that contains the run file in TSV format")
    arser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'evaluation.prototext' will be written: will be created if it does not exist")
    return arser.parse_args()


def main(input_dataset: str, input_run: str, output_dataset: str):
    write_evaluation(read_labels(input_dataset, prefix="labels-"), read_labels(input_run), output_dataset)


if __name__ == '__main__':
    args = parse_args()
    main(args.inputDataset, args.inputRun, args.outputDataset)
