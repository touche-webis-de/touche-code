#!/usr/bin/env python3

"""Evaluator for Human Value Detection 2024 @ CLEF 2024 (Task 2)"""
# Version: 2023-10-15

import argparse
import json
import os
import sys
import warnings
from typing import Union, Dict, Optional, List, Tuple, Literal, Callable

import numpy as np
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


def confidence_attained_constrained(a, b):
    if a == b:
        return 0.5
    return a / (a + b)


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

                    base_frames = [labels_frame.loc[:, id_fields].copy()]

                    skip_file = False
                    for value_prefix in availableValues:
                        value_names = list(filter(
                            lambda col_name: str(col_name).startswith(value_prefix),
                            col_names
                        ))

                        base_frame = pd.DataFrame()
                        base_frame.index = labels_frame.index

                        if len(value_names) == 0:
                            print(
                                "Skipping file {} due to too missing field names for prefix '{}'.".format(
                                    labels_file_name,
                                    value_prefix
                                ))
                            skip_file = True
                            break
                        elif len(value_names) == 1 and value_prefix == value_names[0]:
                            base_frame.loc[:, f"{value_prefix} attained"] = labels_frame.loc[:, value_prefix].clip(0.0, 1.0)
                            base_frame.loc[:, f"{value_prefix} constrained"] = 0.0
                            invalid_col_names.remove(value_names[0])
                        elif len(value_names) == 2 and f"{value_prefix} attained" in value_names and f"{value_prefix} constrained" in value_names:
                            for col_name in value_names:
                                base_frame.loc[:, col_name] = labels_frame.loc[:, col_name].clip(0.0, 1.0)
                                invalid_col_names.remove(col_name)
                        else:
                            print(
                                "Skipping file {} due to too many field names for prefix '{}': '{}'".format(
                                    labels_file_name,
                                    value_prefix,
                                    "', '".join(value_names)
                                ))
                            skip_file = True
                            break
                            pass

                        # calculate confidence and label for subtask 1
                        base_frame.loc[:, f"conf1 {value_prefix}"] = \
                            (base_frame.loc[:, f"{value_prefix} attained"] +
                             base_frame.loc[:, f"{value_prefix} constrained"]).clip(0.0, 1.0)
                        base_frame.loc[:, f"label1 {value_prefix}"] = 0
                        base_frame.loc[
                            base_frame.loc[:, f"conf1 {value_prefix}"] >= 0.5, f"label1 {value_prefix}"] = 1

                        # calculate confidence for subtask 2
                        base_frame.loc[:, f"conf2 {value_prefix} attained"] = base_frame.loc[:, f"{value_prefix} attained"].combine(
                            base_frame.loc[:, f"{value_prefix} constrained"], confidence_attained_constrained,
                            fill_value=0).clip(0.0, 1.0)
                        base_frame.loc[:, f"conf2 {value_prefix} constrained"] = base_frame.loc[:, f"{value_prefix} constrained"].combine(
                            base_frame.loc[:, f"{value_prefix} attained"], confidence_attained_constrained,
                            fill_value=0).clip(0.0, 1.0)

                        # calculate label for subtask 2
                        base_frame.loc[:, f"label2 {value_prefix} attained"] = 0
                        base_frame.loc[base_frame.loc[:, f"conf2 {value_prefix} attained"] >= 0.5, f"label2 {value_prefix} attained"] = 1
                        base_frame.loc[:, f"label2 {value_prefix} constrained"] = 0
                        base_frame.loc[base_frame.loc[:, f"conf2 {value_prefix} constrained"] >= 0.5, f"label2 {value_prefix} constrained"] = 1

                        base_frames.append(base_frame)

                    if skip_file:
                        continue
                    if len(invalid_col_names) > 0:
                        print(
                            "Skipping file {} due to invalid field(s) '{}'".format(
                                labels_file_name,
                                "', '".join(invalid_col_names)
                            ))
                        continue

                    final_base_frame = pd.concat(base_frames, axis=1)

                    for i, row in final_base_frame.iterrows():
                        id_ref = get_id_from_row(id_fields=id_fields, row=row)
                        if available_ids is not None and id_ref not in available_ids:
                            print(f"Skipping line {i} due to unknown ID '{id_ref}'")
                            continue

                        labels[id_ref] = row.to_dict()
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


def initialize_counter(subtask: Literal['1', '2'] = '1') -> Dict[str, int]:
    return {value: 0 for value in get_available_values_by_subtask(subtask)}


def main(
        input_dataset: str,
        input_run: str,
        output_dataset: str,
        id_columns: List[str]):

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

    post_fix = ['(Subtask 1)', '(Subtask 2 - overall)', '(Subtask 2 - attained)', '(Subtask 2 - constrained)']
    precisions, recalls, f1_scores = [[], [], [], []], [[], [], [], []], [[], [], [], []]
    line_precision, line_recall, line_f1_score = [{x: 0 for x in availableValues} for _ in range(4)], \
        [{x: 0 for x in availableValues} for _ in range(4)], [{x: 0 for x in availableValues} for _ in range(4)]
    micro_avg = {'numerator': 0, 'denominator_precision': 0, 'denominator_recall': 0}

    proto_text_body = [[], [], [], []]
    sentence_data_list = [sentence_frame.loc[:, id_columns + ['Text']]]

    roc_data = [[], [], []]

    relevant_values = []

    for value_prefix in availableValues:
        truth_frame = truth_labels.loc[:, [f'label1 {value_prefix}', f'conf1 {value_prefix}']]

        truth_selection = truth_frame.loc[:, f'label1 {value_prefix}'] == 1
        sentence_data = pd.DataFrame()
        sentence_data.index = sentence_frame.index

        # Subtask 1
        eval_dict = run_evaluation_on_value(
            truth_frame[[f'label1 {value_prefix}']],
            run_labels[[f'label1 {value_prefix}']],
            run_labels[[f'conf1 {value_prefix}']],
            f'label1 {value_prefix}'
        )
        if eval_dict is None:
            continue
        else:
            precisions[0].append(eval_dict['metrics']['precision'])
            line_precision[0][value_prefix] = eval_dict['metrics']['precision']
            recalls[0].append(eval_dict['metrics']['recall'])
            line_recall[0][value_prefix] = eval_dict['metrics']['recall']
            f1_scores[0].append(eval_dict['metrics']['f1_score'])
            line_f1_score[0][value_prefix] = eval_dict['metrics']['f1_score']

            roc_data[0].append(
                f"'{value_prefix}': {{label: '{value_prefix}', {eval_dict['roc']}}},"
            )

            sentence_data.loc[:, f"delta {value_prefix}"] = truth_frame.loc[:, f'conf1 {value_prefix}'] - run_labels.loc[:, f'conf1 {value_prefix}']
            sentence_data.loc[:, f"deltaAbs {value_prefix}"] = sentence_data.loc[:, f"delta {value_prefix}"].apply(abs)
            sentence_data.loc[:, f"deltaAttained {value_prefix}"] = 0.0
            sentence_data.loc[:, f"deltaAbsAttained {value_prefix}"] = 0.0
            sentence_data.loc[:, f"deltaConstrained {value_prefix}"] = 0.0
            sentence_data.loc[:, f"deltaAbsConstrained {value_prefix}"] = 0.0

            proto_text_body[0].append(eval_dict['proto_text'])

            relevant_values.append(value_prefix)

        numerator = 0
        denominator_precision = 0
        denominator_recall = 0

        filtered_truth_frame = truth_labels.loc[
            truth_selection,
            [
                f'label2 {value_prefix} attained', f'conf2 {value_prefix} attained',
                f'label2 {value_prefix} constrained', f'conf2 {value_prefix} constrained'
            ]
        ]
        filtered_run_labels = run_labels.loc[
            truth_selection,
            [
                f'label2 {value_prefix} attained', f'conf2 {value_prefix} attained',
                f'label2 {value_prefix} constrained', f'conf2 {value_prefix} constrained'
            ]
        ]

        # Subtask 2 attained
        eval_dict = run_evaluation_on_value(
            filtered_truth_frame[[f'label2 {value_prefix} attained']],
            filtered_run_labels[[f'label2 {value_prefix} attained']],
            filtered_run_labels[[f'conf2 {value_prefix} attained']],
            f'label2 {value_prefix} attained'
        )
        if eval_dict is not None:
            precisions[2].append(eval_dict['metrics']['precision'])
            line_precision[2][value_prefix] = eval_dict['metrics']['precision']
            recalls[2].append(eval_dict['metrics']['recall'])
            line_recall[2][value_prefix] = eval_dict['metrics']['recall']
            f1_scores[2].append(eval_dict['metrics']['f1_score'])
            line_f1_score[2][value_prefix] = eval_dict['metrics']['f1_score']

            roc_data[1].append(
                f"'{value_prefix}': {{label: '{value_prefix}', {eval_dict['roc']}}},"
            )

            numerator += eval_dict['micro_avg']['numerator']
            denominator_precision += eval_dict['micro_avg']['denominator_precision']
            denominator_recall += eval_dict['micro_avg']['denominator_recall']

            sentence_data.loc[truth_selection, f"deltaAttained {value_prefix}"] = \
                filtered_truth_frame.loc[:, f'conf2 {value_prefix} attained'] - \
                filtered_run_labels.loc[:, f'conf2 {value_prefix} attained']
            sentence_data.loc[:, f"deltaAbsAttained {value_prefix}"] = \
                sentence_data.loc[:, f"deltaAttained {value_prefix}"].apply(abs)

            proto_text_body[2].append(eval_dict['proto_text'])

        # Subtask 2 constrained
        eval_dict = run_evaluation_on_value(
            filtered_truth_frame[[f'label2 {value_prefix} constrained']],
            filtered_run_labels[[f'label2 {value_prefix} constrained']],
            filtered_run_labels[[f'conf2 {value_prefix} constrained']],
            f'label2 {value_prefix} constrained'
        )
        if eval_dict is not None:
            precisions[3].append(eval_dict['metrics']['precision'])
            line_precision[3][value_prefix] = eval_dict['metrics']['precision']
            recalls[3].append(eval_dict['metrics']['recall'])
            line_recall[3][value_prefix] = eval_dict['metrics']['recall']
            f1_scores[3].append(eval_dict['metrics']['f1_score'])
            line_f1_score[3][value_prefix] = eval_dict['metrics']['f1_score']

            roc_data[2].append(
                f"'{value_prefix}': {{label: '{value_prefix}', {eval_dict['roc']}}},"
            )

            numerator += eval_dict['micro_avg']['numerator']
            denominator_precision += eval_dict['micro_avg']['denominator_precision']
            denominator_recall += eval_dict['micro_avg']['denominator_recall']

            sentence_data.loc[truth_selection, f"deltaConstrained {value_prefix}"] = \
                filtered_truth_frame.loc[:, f'conf2 {value_prefix} constrained'] - \
                filtered_run_labels.loc[:, f'conf2 {value_prefix} constrained']
            sentence_data.loc[:, f"deltaAbsConstrained {value_prefix}"] = \
                sentence_data.loc[:, f"deltaConstrained {value_prefix}"].apply(abs)

            proto_text_body[3].append(eval_dict['proto_text'])

        # Subtask 2 overall
        micro_precision = numerator / denominator_precision if denominator_precision > 0 else 0.0
        precisions[1].append(micro_precision)
        line_precision[1][value_prefix] = micro_precision
        micro_recall = numerator / denominator_recall if denominator_recall > 0 else 0.0
        recalls[1].append(micro_recall)
        line_recall[1][value_prefix] = micro_recall
        micro_f1_score = 2 * micro_precision * micro_recall / (micro_precision + micro_recall) \
            if micro_precision + micro_recall > 0.0 else 0.0
        f1_scores[1].append(micro_f1_score)
        line_f1_score[1][value_prefix] = micro_f1_score

        proto_text_body[1].append(
            f'measure {{\n key: "Precision {value_prefix} (Subtask 2 - overall)"\n value: "{micro_precision}"\n}}\n'
            f'measure {{\n key: "Recall {value_prefix} (Subtask 2 - overall)"\n value: "{micro_recall}"\n}}\n'
            f'measure {{\n key: "F1 {value_prefix} (Subtask 2 - overall)"\n value: "{micro_f1_score}"\n}}\n'
        )

        micro_avg['numerator'] += numerator
        micro_avg['denominator_precision'] += denominator_precision
        micro_avg['denominator_recall'] += denominator_recall

        sentence_data_list.append(sentence_data)

    avg_precision = [0, 0, 0, 0]
    avg_recall = [0, 0, 0, 0]
    avg_f1_score = [0, 0, 0, 0]

    # calculate macro_avg
    for i in [0, 2, 3]:
        macro_precision = sum(precisions[i]) / len(precisions[i]) if len(precisions[i]) > 0 else 0.0
        avg_precision[i] = macro_precision
        macro_recall = sum(recalls[i]) / len(recalls[i]) if len(recalls[i]) > 0 else 0.0
        avg_recall[i] = macro_recall
        avg_f1_score[i] = 2 * macro_precision * macro_recall / (macro_precision + macro_recall) \
            if macro_precision + macro_recall > 0.0 else 0.0

    # calculate micro_avg
    micro_precision = micro_avg['numerator'] / micro_avg['denominator_precision'] \
        if micro_avg['denominator_precision'] > 0 else 0.0
    avg_precision[1] = micro_precision
    micro_recall = micro_avg['numerator'] / micro_avg['denominator_recall'] \
        if micro_avg['denominator_recall'] > 0 else 0.0
    avg_recall[1] = micro_recall
    avg_f1_score[1] = 2 * micro_precision * micro_recall / (micro_precision + micro_recall) \
        if micro_precision + micro_recall > 0.0 else 0.0

    # combine sentence data for GUI table
    final_sentence_data = pd.concat(sentence_data_list, axis=1).round(2)

    ##################################
    # Write evaluation.prototext #####
    ##################################

    with open(os.path.join(output_dataset, "evaluation.prototext"), "w") as evaluationFile:
        for i in range(4):
            evaluationFile.write(
                f'measure {{\n key: "Precision {post_fix[i]}"\n value: "{avg_precision[i]}"\n}}\n'
                f'measure {{\n key: "Recall {post_fix[i]}"\n value: "{avg_recall[i]}"\n}}\n'
                f'measure {{\n key: "F1 {post_fix[i]}"\n value: "{avg_f1_score[i]}"\n}}\n'
            )
        for i in range(4):
            evaluationFile.write(''.join(proto_text_body[i]))

    ####################
    # Write to GUI #####
    ####################

    # overview table
    table_data = f"[{{metric: 'F1', subtask1: {avg_f1_score[0]:.2f}, subtask2: {avg_f1_score[1]:.2f}, subtask2Attained: {avg_f1_score[2]:.2f}, subtask2Constrained: {avg_f1_score[3]:.2f}}},\n" \
                 f"{{metric: 'Precision', subtask1: {avg_precision[0]:.2f}, subtask2: {avg_precision[1]:.2f}, subtask2Attained: {avg_precision[2]:.2f}, subtask2Constrained: {avg_precision[3]:.2f}}},\n" \
                 f"{{metric: 'Recall', subtask1: {avg_recall[0]:.2f}, subtask2: {avg_recall[1]:.2f}, subtask2Attained: {avg_recall[2]:.2f}, subtask2Constrained: {avg_recall[3]:.2f}}}]"

    gui_function_general_data = "function general_data() {\nreturn " \
                                f"{table_data}\n" \
                                "}"

    # with open(os.path.join(output_dataset, "evaluation1.txt"), "w") as evaluationFile:
    #     evaluationFile.write(table_data)

    # line plot data
    line_data = "{\n" \
                "subtask1: { plot1: [\n" \
                f"{{label: 'F1-Score', pointStyle: 'circle', pointRadius: 5, borderColor: 'rgb(36,93,215)', backgroundColor: 'rgba(36,93,215,0.2)', data: [{', '.join(str(x) for x in line_f1_score[0].values())}]}}\n" \
                "], plot2: [\n" \
                f"{{label: 'Precision', pointStyle: 'rectRot', pointRadius: 5, borderColor: 'rgb(36,93,215)', backgroundColor: 'rgba(36,93,215,0.2)', data: [{', '.join(str(x) for x in line_precision[0].values())}]}},\n" \
                f"{{label: 'Recall', pointStyle: 'triangle', pointRadius: 5, borderColor: 'rgb(36,93,215)', backgroundColor: 'rgba(36,93,215,0.2)', data: [{', '.join(str(x) for x in line_recall[0].values())}]}}\n" \
                "]}, subtask2: { plot1: [\n" \
                f"{{label: 'F1-Score (overall)', pointStyle: 'circle', pointRadius: 5, borderColor: 'rgb(36,93,215)', backgroundColor: 'rgba(36,93,215,0.2)', data: [{', '.join(str(x) for x in line_f1_score[1].values())}]}},\n" \
                f"{{label: 'F1-Score (attained)', pointStyle: 'circle', pointRadius: 5, borderColor: 'rgb(43,203,184)', backgroundColor: 'rgba(43,203,184,0.2)', data: [{', '.join(str(x) for x in line_f1_score[2].values())}]}},\n" \
                f"{{label: 'F1-Score (constrained)', pointStyle: 'circle', pointRadius: 5, borderColor: 'rgb(235,111,54)', backgroundColor: 'rgba(235,111,54,0.2)', data: [{', '.join(str(x) for x in line_f1_score[3].values())}]}}\n" \
                "], plot2: [\n" \
                f"{{label: 'Precision (overall)', pointStyle: 'rectRot', pointRadius: 5, borderColor: 'rgb(36,93,215)', backgroundColor: 'rgba(36,93,215,0.2)', data: [{', '.join(str(x) for x in line_precision[1].values())}]}},\n" \
                f"{{label: 'Precision (attained)', pointStyle: 'rectRot', pointRadius: 5, borderColor: 'rgb(43,203,184)', backgroundColor: 'rgba(43,203,184,0.2)', data: [{', '.join(str(x) for x in line_precision[2].values())}]}},\n" \
                f"{{label: 'Precision (constrained)', pointStyle: 'rectRot', pointRadius: 5, borderColor: 'rgb(235,111,54)', backgroundColor: 'rgba(235,111,54,0.2)', data: [{', '.join(str(x) for x in line_precision[3].values())}]}},\n" \
                f"{{label: 'Recall (overall)', pointStyle: 'triangle', pointRadius: 5, borderColor: 'rgb(36,93,215)', backgroundColor: 'rgba(36,93,215,0.2)', data: [{', '.join(str(x) for x in line_recall[1].values())}]}},\n" \
                f"{{label: 'Recall (attained)', pointStyle: 'triangle', pointRadius: 5, borderColor: 'rgb(43,203,184)', backgroundColor: 'rgba(43,203,184,0.2)', data: [{', '.join(str(x) for x in line_recall[2].values())}]}},\n" \
                f"{{label: 'Recall (constrained)', pointStyle: 'triangle', pointRadius: 5, borderColor: 'rgb(235,111,54)', backgroundColor: 'rgba(235,111,54,0.2)', data: [{', '.join(str(x) for x in line_recall[3].values())}]}}\n" \
                "]}\n}"

    gui_function_line_plot_data = "function line_plot_data() {\nreturn " \
                                  f"{line_data}\n" \
                                  "}"

    # with open(os.path.join(output_dataset, "evaluation2.txt"), "w") as evaluationFile:
    #     evaluationFile.write(line_data)

    # sentence data
    sentence_row_id = 0
    sentence_lines = ['[']
    for _, row in final_sentence_data.iterrows():
        sentence_lines.append(
            f"{str({'id': sentence_row_id, **row})},"
        )
        sentence_row_id += 1
    sentence_lines.append(']')
    full_sentence_lines = '\n'.join(sentence_lines)

    gui_function_sentence_data = "function sentence_data() {\nreturn {\n" \
                                 f"values: {str(relevant_values)},\n" \
                                 f"tableData: {full_sentence_lines}\n" \
                                 "}\n}"

    # with open(os.path.join(output_dataset, "evaluation3.txt"), "w") as evaluationFile:
    #     evaluationFile.write(str(relevant_values))
    #     evaluationFile.write('\n')
    #     evaluationFile.write('\n'.join(sentence_lines))

    # ROC curve data
    roc_plot1 = '\n'.join(roc_data[0])
    roc_plot2 = '\n'.join(roc_data[1])
    roc_plot3 = '\n'.join(roc_data[2])
    full_roc_plots = "[\n{\n" \
                     f"{roc_plot1}\n" \
                     "},\n{\n" \
                     f"{roc_plot2}\n" \
                     "},\n{\n" \
                     f"{roc_plot3}\n" \
                     "}\n]"

    gui_function_value_roc_curve = "function value_roc_curve() {\nreturn " \
                                   f"{full_roc_plots}\n" \
                                   "}"

    # with open(os.path.join(output_dataset, "evaluation_roc.txt"), "w") as evaluationFile:
    #     evaluationFile.write(full_roc_plots)

    if not os.path.exists('index.html'):
        print('No index.html found.')
    else:
        with open('index.html', 'r') as gui_file:
            gui_lines = gui_file.readlines()

        start_index, end_index = -1, -1
        for i in range(len(gui_lines)):
            if start_index == -1 and "/* START DATA INJECT */" in gui_lines[i]:
                start_index = i
            elif "/* END DATA INJECT */" in gui_lines[i]:
                end_index = i
                break
        if end_index == -1:
            sys.exit("index.html can't be parsed correctly")

        reformatted_start_line = gui_lines[start_index][:gui_lines[start_index].find("/* START DATA INJECT */")]
        reformatted_end_line = gui_lines[end_index][
                                   gui_lines[end_index].rfind("/* END DATA INJECT */") + len("/* END DATA INJECT */"):
                               ]

        new_gui_lines = gui_lines[:start_index] + [
            reformatted_start_line,
            gui_function_general_data,
            '\n\n',
            gui_function_value_roc_curve,
            '\n\n',
            gui_function_line_plot_data,
            '\n\n',
            gui_function_sentence_data,
            '\n',
            reformatted_end_line
        ] + gui_lines[end_index + 1:]

        with open(os.path.join(output_dataset, "index.html"), "w") as gui_file:
            gui_file.writelines(new_gui_lines)


def run_evaluation_on_value(
        truth_labels: pd.DataFrame,
        run_labels: pd.DataFrame,
        run_labels_confidence: pd.DataFrame,
        value_name: str):

    actual_value_name = value_name[7:]
    num_instances = len(truth_labels)

    # calculate roc curves
    truth_labels_stack = truth_labels.stack()
    run_labels_stack = run_labels_confidence.stack()

    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=UndefinedMetricWarning)
        fpr, tpr, thresholds = metrics.roc_curve(y_true=truth_labels_stack.values, y_score=run_labels_stack.values)
    threshold_0_5_position = None
    try:
        roc_auc = f"AUC: {metrics.roc_auc_score(y_true=truth_labels_stack.values, y_score=run_labels_stack.values):.2f}"
        if 0.5 in thresholds:
            threshold_0_5_position = np.where(thresholds, 0.5)
        else:
            threshold_0_5_position = len(thresholds)
            for i in range(len(thresholds) - 1):
                if (thresholds[i] == float('inf') and 0.5 > thresholds[i+1]) or \
                        (thresholds[i] != float('inf') and thresholds[i] > 0.5 > thresholds[i+1]):
                    threshold_0_5_position = i + 1
                    break
    except ValueError:
        # only one label present
        roc_auc = 'AUC: undefined'
        fpr = []
        tpr = []

    # calculate F1
    relevants = 0
    positives = 0
    true_positives = 0
    true_negatives = 0

    for idx, row in truth_labels.iterrows():
        corresponding_run_label = run_labels.loc[idx, value_name]

        for value, truth_label in row.items():
            if truth_label == 1:
                relevants += 1
                if corresponding_run_label == 1:
                    positives += 1
                    true_positives += 1
                else:
                    pass
            elif corresponding_run_label == 1:
                positives += 1
            else:
                true_negatives += 1

    if relevants != 0:
        if threshold_0_5_position is not None:
            # TPR = TP / (TP + FN)
            new_tpr = true_positives / relevants
            # FPR = FP / (FP + TN)
            new_fpr = (positives - true_positives) / (positives - true_positives + true_negatives) if (positives - true_positives + true_negatives) > 0 else 0.0

            tpr = np.insert(tpr, threshold_0_5_position, new_tpr)
            fpr = np.insert(fpr, threshold_0_5_position, new_fpr)

        roc_entry = ["showLine: true, fill: true, pointRadius: 4, backgroundColor: 'rgb(235,111,54,0.2)',"]
        if len(tpr) > 0:
            border_colors = ["'rgb(235,111,54)'"] * len(tpr)
            border_colors[threshold_0_5_position] = "'rgb(255,0,0)'"
            roc_entry.append(f"borderColor: [ {', '.join(border_colors)} ],")

            data_records = []
            for i in range(len(tpr)):
                data_records.append(f"{{x: {fpr[i]}, y: {tpr[i]}}}")
            roc_entry.append(f"data: [ {', '.join(data_records)} ],")
        else:
            roc_entry.append('borderColor: [], data: [],')
        roc_entry.append(f"auc: '{roc_auc}'")

        precision = 0 if positives == 0 else true_positives / positives
        recall = true_positives / relevants
        f1_score = 2 * precision * recall / (precision + recall) if precision + recall > 0.0 else 0.0

        proto_text = f'measure {{\n key: "Precision {actual_value_name}"\n value: "{precision}"\n}}\n' \
                     f'measure {{\n key: "Recall {actual_value_name}"\n value: "{recall}"\n}}\n' \
                     f'measure {{\n key: "F1 {actual_value_name}"\n value: "{f1_score}"\n}}\n'

        return {
            'metrics': {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            },
            'micro_avg': {
                'numerator': true_positives,
                'denominator_precision': positives,
                'denominator_recall': relevants
            },
            'roc': ' '.join(roc_entry),
            'proto_text': proto_text
        }

    else:
        return None


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
        '--id-columns', type=str, nargs='*', required=False, default=['Text-ID', 'Sentence-ID'],
        help="")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.inputDataset, args.inputRun, args.outputDataset, id_columns=args.id_columns)
