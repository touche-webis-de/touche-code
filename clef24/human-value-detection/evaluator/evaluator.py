#!/usr/bin/env python3

"""Evaluator for Human Value Detection 2024 @ CLEF 2024 (Task 2)"""
# Version: 2023-10-15

import argparse
import json
import os
import sys
import warnings
from typing import Union, Dict, Optional, List, Tuple, Literal, Callable

import pandas as pd
from sklearn import metrics
from sklearn.exceptions import UndefinedMetricWarning

# level 1
# availableValues = ["Be ambitious", "Be behaving properly", "Be broadminded", "Be capable", "Be choosing own goals", "Be compliant", "Be courageous", "Be creative", "Be curious", "Be daring", "Be forgiving", "Be helpful", "Be holding religious faith", "Be honest", "Be honoring elders", "Be humble", "Be independent", "Be intellectual", "Be just", "Be logical", "Be loving", "Be neat and tidy", "Be polite", "Be protecting the environment", "Be respecting traditions", "Be responsible", "Be self-disciplined", "Have a comfortable life", "Have a good reputation", "Have an exciting life", "Have an objective view", "Have a safe country", "Have a sense of belonging", "Have a stable society", "Have a varied life", "Have a world at peace", "Have a world of beauty", "Have equality", "Have freedom of action", "Have freedom of thought", "Have good health", "Have harmony with nature", "Have influence", "Have life accepted as is", "Have loyalty towards friends", "Have no debts", "Have pleasure", "Have privacy", "Have social recognition", "Have success", "Have the own family secured", "Have the right to command", "Have the wisdom to accept others", "Have wealth"]
# level 2
availableValues = ["Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance"]
availableValuesSubtask2 = [value + postfix for value in availableValues for postfix in [' attained', ' constrained']]


def get_available_values_by_subtask(subtask: Literal['1', '2'] = '1'):
    return availableValues if subtask == '1' else availableValuesSubtask2


def read_labels(
        directory: str,
        prefix: Optional[str] = None,
        id_fields: List[str] = None,
        available_ids: Optional[List] = None) -> pd.DataFrame:
    if id_fields is None:
        id_fields = ['Text-ID', 'Sentence-ID']

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

                    missing_id_fields = list(filter(
                        lambda id_field: id_field not in col_names,
                        id_fields))
                    if len(missing_id_fields) > 0:
                        print(
                            "Skipping file {} due to missing field(s) '{}'".format(
                                labels_file_name,
                                "', '".join(missing_id_fields)
                            ))
                        continue

                    invalid_col_names = list(filter(
                        lambda col_name: not (col_name in id_fields or col_name.startswith('Universalism: objectivity')),
                        col_names
                    ))
                    col_name_map = {}
                    for value_prefix in availableValues:
                        value_names = list(filter(
                            lambda col_name: str(col_name).startswith(value_prefix),
                            col_names
                        ))
                        if len(value_names) == 1 and value_prefix == value_names[0]:
                            col_name_map[value_names[0]] = f"{value_prefix} attained"
                            labels_frame[f"{value_prefix} constrained"] = 0.0
                            col_name_map[f"{value_prefix} constrained"] = f"{value_prefix} constrained"
                            invalid_col_names.remove(value_names[0])
                        elif len(value_names) == 2 and f"{value_prefix} attained" in value_names and f"{value_prefix} constrained" in value_names:
                            for col_name in value_names:
                                col_name_map[col_name] = col_name
                                invalid_col_names.remove(col_name)
                        else:
                            print(
                                "Skipping file {} due to too many field names for prefix '{}': '{}'".format(
                                    labels_file_name,
                                    value_prefix,
                                    "', '".join(value_names)
                                ))
                            continue
                    if len(invalid_col_names) > 0:
                        print(
                            "Skipping file {} due to invalid field(s) '{}'".format(
                                labels_file_name,
                                "', '".join(invalid_col_names)
                            ))
                        continue

                    labels_frame = labels_frame.rename(columns=col_name_map)
                    present_values = list(col_name_map.values())
                    if len(set(present_values)) < len(present_values):
                        print(f"Skipping file {labels_file_name} due to duplicate field refs")
                        continue

                    for i, row in labels_frame.iterrows():
                        id_ref = get_id_from_row(id_fields=id_fields, row=row)
                        if available_ids is not None and id_ref not in available_ids:
                            print(f"Skipping line {i} due to unknown ID '{id_ref}'")
                            continue
                        row_values = row[present_values].to_dict()

                        invalid_labels = [label for label, value in row_values.items() if not (0.0 <= value <= 1.0)]
                        if len(invalid_labels) > 0:
                            print(f"Skipping line {i} due to invalid label(s) '{invalid_labels}'")
                            continue

                        labels[id_ref] = row_values
    if len(labels) == 0:
        raise OSError(
            "No {}labels found in directory '{}'".format(
                '' if prefix is None else f'\'{prefix}\' ',
                directory
            )
        )
    return pd.DataFrame.from_dict(labels, orient='index')


def get_id_from_row(id_fields: List[str], row):
    id_tuple = tuple(row[x] for x in id_fields)
    if len(id_tuple) == 1:
        return id_tuple[0]
    return id_tuple


def format_for_subtask_1(frame: pd.DataFrame):
    col_names = frame.columns
    format_frame = pd.DataFrame(index=frame.index)

    for value_name in availableValues:
        if f"{value_name} attained" in col_names:
            format_frame[value_name] = frame[[f"{value_name} attained", f"{value_name} constrained"]].sum(axis=1)

    return format_frame


def apply_majority_class(frame: pd.DataFrame, subtask: Literal['1', '2'] = '1', epsilon: float = 0.000001):
    col_names = frame.columns

    if subtask == '1':
        for value_name in availableValues:
            if value_name in col_names:
                frame[value_name] = frame[value_name].apply(lambda x: 1 if x >= 0.5 - epsilon else 0).astype(int)
    else:
        for value_name in availableValues:
            if f"{value_name} attained" in col_names:
                none_axis: pd.Series = frame[[f"{value_name} attained", f"{value_name} constrained"]].sum(axis=1).apply(
                    lambda x: 1 - x)
                for idx, _ in frame.iterrows():
                    value_attained = frame.loc[idx, f"{value_name} attained"]
                    value_constrained = frame.loc[idx, f"{value_name} constrained"]
                    frame.loc[idx, f"{value_name} attained"] = (
                        1 if value_attained >= value_constrained - epsilon and value_attained >= none_axis.loc[
                            idx] - epsilon else 0
                    )
                    frame.loc[idx, f"{value_name} constrained"] = (
                        1 if value_constrained >= value_attained - epsilon and value_constrained >= none_axis.loc[
                            idx] - epsilon else 0
                    )
                frame[f"{value_name} attained"] = frame[f"{value_name} attained"].astype(int)
                frame[f"{value_name} constrained"] = frame[f"{value_name} constrained"].astype(int)

    return frame


def initialize_counter(subtask: Literal['1', '2'] = '1') -> Dict[str, int]:
    return {value: 0 for value in get_available_values_by_subtask(subtask)}


def main(
        input_dataset: str,
        input_run: str,
        output_dataset: str,
        id_columns: List[str],
        subtask: Literal['1', '2'] = '1'):

    truth_labels = read_labels(input_dataset, prefix="labels-", id_fields=id_columns)
    sentence_frame = pd.read_csv(os.path.join(input_dataset, "sentences.tsv"), sep='\t', index_col=None, header=0)
    sentence_frame.index = pd.MultiIndex.from_tuples(list(zip(*[sentence_frame[c] for c in id_columns])))

    run_labels = read_labels(input_run, id_fields=id_columns)

    # filter column level
    truth_columns = list(truth_labels.columns)
    present_columns = list(filter(lambda x: x in truth_columns, run_labels.columns))

    missing_columns = len(truth_columns) - len(present_columns)
    if missing_columns > 0:
        # convert to print if subsets of values are allowed
        sys.exit(f"{missing_columns} columns missing in prediction data")

    # filter row level
    run_labels: pd.DataFrame = run_labels.loc[run_labels.index.isin(truth_labels.index)]
    all_instances = truth_labels.shape[0]
    truth_labels: pd.DataFrame = truth_labels.loc[truth_labels.index.isin(run_labels.index)]

    missing_rows = all_instances - truth_labels.shape[0]
    if missing_rows > 0:
        sys.exit(f"{missing_rows} instances missing in prediction data")

    num_instances = len(truth_labels)
    print(f"Truth labels: {num_instances}\nRun labels:   {len(run_labels)}")

    if not os.path.exists(output_dataset):
        os.makedirs(output_dataset)

    eval_object_both = run_evaluation(
        truth_labels=apply_majority_class(format_for_subtask_1(frame=truth_labels), subtask='1'),
        run_labels=apply_majority_class(format_for_subtask_1(frame=run_labels), subtask='1'),
        run_labels_confidence=format_for_subtask_1(frame=run_labels),
        sentence_frame=sentence_frame,
        subtask='1',
        postfix=''
    )
    if subtask == '2':
        truth_labels = apply_majority_class(truth_labels, subtask='2')
        eval_object_attained = run_evaluation(
            truth_labels=truth_labels.filter(regex='attained$'),
            run_labels=apply_majority_class(run_labels, subtask='2').filter(regex='attained$'),
            run_labels_confidence=run_labels.filter(regex='attained$'),
            sentence_frame=sentence_frame,
            subtask='2',
            postfix=' attained'
        )
        eval_object_constrained = run_evaluation(
            truth_labels=truth_labels.filter(regex='constrained$'),
            run_labels=apply_majority_class(run_labels, subtask='2').filter(regex='constrained$'),
            run_labels_confidence=run_labels.filter(regex='constrained$'),
            sentence_frame=sentence_frame,
            subtask='2',
            postfix=' constrained'
        )

    with open(os.path.join(output_dataset, "evaluation.prototext"), "w") as evaluationFile:
        evaluationFile.write(eval_object_both['proto_text']['header'])
        if subtask == '2':
            evaluationFile.write(eval_object_attained['proto_text']['header'])
            evaluationFile.write(eval_object_constrained['proto_text']['header'])

        evaluationFile.write(eval_object_both['proto_text']['body'])
        if subtask == '2':
            evaluationFile.write(eval_object_attained['proto_text']['body'])
            evaluationFile.write(eval_object_constrained['proto_text']['body'])

    sentence_details = eval_object_both['detail']
    if subtask == '2':
        sentence_details = sentence_details.join(
            eval_object_attained['detail'].drop(columns='Text')
        ).join(
            eval_object_constrained['detail'].drop(columns='Text')
        )
    sentence_detail_list = [
        {
            **{name: value for name, value in zip(id_columns, list(idx))},
            **record
        } for idx, record in sentence_details.to_dict('index').items()
    ]

    if subtask == '1':
        eval_object = {
            'sub_task': '1',
            'roc': {
                'tpr': eval_object_both['roc']['tpr'],
                'fpr': eval_object_both['roc']['fpr'],
                'auc': eval_object_both['roc']['auc'],
            },
            'global': {
                'f1_score': eval_object_both['global']['f1_score'],
                'precision': eval_object_both['global']['precision'],
                'recall': eval_object_both['global']['recall'],
                'list_f1_score': eval_object_both['global']['list_f1_score'],
                'list_precision': eval_object_both['global']['list_precision'],
                'list_recall': eval_object_both['global']['list_recall'],
            },
            'detail': sentence_detail_list
        }
    else:
        eval_object = {
            'sub_task': '2',
            'roc': {
                'tpr': eval_object_both['roc']['tpr'],
                'fpr': eval_object_both['roc']['fpr'],
                'auc': eval_object_both['roc']['auc'],
                'tpr_attained': eval_object_attained['roc']['tpr'],
                'fpr_attained': eval_object_attained['roc']['fpr'],
                'auc_attained': eval_object_attained['roc']['auc'],
                'tpr_constrained': eval_object_constrained['roc']['tpr'],
                'fpr_constrained': eval_object_constrained['roc']['fpr'],
                'auc_constrained': eval_object_constrained['roc']['auc']
            },
            'global': {
                'f1_score': eval_object_both['global']['f1_score'],
                'precision': eval_object_both['global']['precision'],
                'recall': eval_object_both['global']['recall'],
                'list_f1_score': eval_object_both['global']['list_f1_score'],
                'list_precision': eval_object_both['global']['list_precision'],
                'list_recall': eval_object_both['global']['list_recall'],
                'f1_score_attained': eval_object_attained['global']['f1_score'],
                'precision_attained': eval_object_attained['global']['precision'],
                'recall_attained': eval_object_attained['global']['recall'],
                'list_f1_score_attained': eval_object_attained['global']['list_f1_score'],
                'list_precision_attained': eval_object_attained['global']['list_precision'],
                'list_recall_attained': eval_object_attained['global']['list_recall'],
                'f1_score_constrained': eval_object_constrained['global']['f1_score'],
                'precision_constrained': eval_object_constrained['global']['precision'],
                'recall_constrained': eval_object_constrained['global']['recall'],
                'list_f1_score_constrained': eval_object_constrained['global']['list_f1_score'],
                'list_precision_constrained': eval_object_constrained['global']['list_precision'],
                'list_recall_constrained': eval_object_constrained['global']['list_recall'],
            },
            'detail': sentence_detail_list
        }

    # Write to GUI (currently dump JSON)
    with open(os.path.join(output_dataset, "evaluation.json"), "w") as evaluationJSON:
        json.dump(eval_object, evaluationJSON)


def run_evaluation(
        truth_labels: pd.DataFrame,
        run_labels: pd.DataFrame,
        run_labels_confidence: pd.DataFrame,
        sentence_frame: pd.DataFrame,
        subtask: Literal['1', '2'] = '1',
        postfix: Literal['', ' attained', ' constrained'] = ''):

    num_instances = len(truth_labels)

    # calculate roc curves
    truth_labels_stack = truth_labels.stack()
    run_labels_stack = run_labels_confidence.stack()

    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=UndefinedMetricWarning)
        tpr, fpr, _ = metrics.roc_curve(y_true=truth_labels_stack.values, y_score=run_labels_stack.values)
    try:
        roc_auc = metrics.roc_auc_score(y_true=truth_labels_stack.values, y_score=run_labels_stack.values)
    except ValueError:
        # only one label present
        roc_auc = 'undefined'

    # calculate F1
    relevants = initialize_counter(subtask=subtask)
    positives = initialize_counter(subtask=subtask)
    true_positives = initialize_counter(subtask=subtask)
    true_negatives = initialize_counter(subtask=subtask)

    sentence_details = {}

    for idx, row in truth_labels.iterrows():
        corresponding_run_labels = run_labels.loc[idx]

        sentence_data = {'Text': sentence_frame.loc[idx, 'Text']}

        tps, fns, fps = 0, 0, 0

        for value, truth_label in row.items():
            if truth_label == 1:
                relevants[str(value)] += 1
                if corresponding_run_labels is not None:
                    if corresponding_run_labels[value] == 1:
                        positives[str(value)] += 1
                        true_positives[str(value)] += 1
                        tps += 1
                    else:
                        fns += 1
            elif corresponding_run_labels is not None:
                if corresponding_run_labels[value] == 1:
                    positives[str(value)] += 1
                    fps += 1
                else:
                    true_negatives[str(value)] += 1


        all_relevants = tps + fns
        sentence_data[
            'TP' + postfix] = "0" if all_relevants == 0 else f"{tps}/{all_relevants} ({round(tps / all_relevants * 100, 1)}%)"
        sentence_data['FN' + postfix] = "0" if all_relevants == 0 else f"{fns}/{all_relevants}"
        sentence_data['FP' + postfix] = fps

        sentence_details[idx] = sentence_data

    precisions: Dict[str, float] = {
        value: 0 if positives[value] == 0 else true_positives[value] / positives[value]
        for value in get_available_values_by_subtask(subtask) if relevants[value] != 0
    }
    recalls: Dict[str, float] = {
        value: true_positives[value] / relevants[value]
        for value in get_available_values_by_subtask(subtask) if relevants[value] != 0
    }
    f1_scores: Dict[str, float] = {
        value: 0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
        for (value, precision), recall in zip(precisions.items(), recalls.values())
    }
    accuracies: Dict[str, float] = {
        value: 0 if num_instances == 0 else (true_positives[value] + true_negatives[value]) / num_instances
        for value in get_available_values_by_subtask(subtask) if relevants[value] != 0
    }

    precision = sum(precisions.values()) / len(precisions) if len(precisions) > 0 else 0.0
    recall = sum(recalls.values()) / len(recalls) if len(recalls) > 0 else 0.0
    f1_score = 2 * precision * recall / (precision + recall) if precision + recall > 0.0 else 0.0
    accuracy = sum(accuracies.values()) / len(accuracies) if len(accuracies) > 0 else 0.0

    proto_text_header = f'measure {{\n key: "Precision{postfix}"\n value: "{precision}"\n}}\n' \
                        f'measure {{\n key: "Recall{postfix}"\n value: "{recall}"\n}}\n' \
                        f'measure {{\n key: "F1{postfix}"\n value: "{f1_score}"\n}}\n' \
                        f'measure {{\n key: "Accuracy{postfix}"\n value: "{accuracy}"\n}}\n'
    proto_text_list = []
    for value in get_available_values_by_subtask(subtask):
        if value in precisions.keys():
            proto_text_list.append(
                f'measure {{\n key: "Precision {value}"\n value: "{precisions[value]}"\n}}\n'
                f'measure {{\n key: "Recall {value}"\n value: "{recalls[value]}"\n}}\n'
                f'measure {{\n key: "F1 {value}"\n value: "{f1_scores[value]}"\n}}\n'
                f'measure {{\n key: "Accuracy {value}"\n value: "{accuracies[value]}"\n}}\n'
            )
    proto_text_body = "".join(proto_text_list)

    return {
        'proto_text': {
            'header': proto_text_header,
            'body': proto_text_body
        },
        'roc': {
            'tpr': list(tpr),
            'fpr': list(fpr),
            'auc': roc_auc
        },
        'global': {
            'f1_score': f1_score,
            'precision': precision,
            'recall': recall,
            'list_f1_score': f1_scores,
            'list_precision': precisions,
            'list_recall': recalls,
        },
        'detail': pd.DataFrame.from_dict(sentence_details, orient='index')
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluator for Human Value Detection 2024 @ CLEF 2024")
    parser.add_argument(
        "-i", "--inputDataset", type=str, required=True,
        help="Directory that contains the input dataset, at least the 'labels-*.tsv'")
    parser.add_argument(
        "-r", "--inputRun", type=str, required=True,
        help="Directory that contains the run file in TSV format")
    parser.add_argument(
        "-o", "--outputDataset", type=str, required=True,
        help="Directory to which the 'evaluation.prototext' will be written: will be created if it does not exist")
    parser.add_argument(
        "-s", "--sub-task", type=str, choices=['1', '2'], required=False, default='1',
        help="")
    parser.add_argument(
        '--id-columns', type=str, nargs='*', required=False, default=['Text-ID', 'Sentence-ID'],
        help="")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.inputDataset, args.inputRun, args.outputDataset, id_columns=args.id_columns, subtask=args.sub_task)
