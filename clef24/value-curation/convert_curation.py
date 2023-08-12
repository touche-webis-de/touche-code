#!/usr/bin/env python3

import argparse
import json
from typing import Union, List

import sys
import os

import zipfile
import re

import pandas as pd


########################
# START: CONSTANTS #####
########################

_text_id_ref = 'Text-ID'
_sentence_id_ref = 'Sentence-ID'
_text_ref = 'Text'
_label_ref = 'Label'
_attainment_ref = 'Attainment'
_value_list = ["Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance"]
_value_dictionary = {value.replace(':', ' -').upper(): value for value in _value_list}

######################
# END: CONSTANTS #####
######################


def _find_file_by_name(current_path: str, target_file: str) -> List[str]:
    if os.path.isfile(current_path):

        if current_path.endswith('.zip'):
            current_directory = os.path.dirname(current_path)
            with zipfile.ZipFile(current_path, 'r') as zip_arc:
                name_list = zip_arc.namelist()
                zip_arc.extractall(current_directory)

            files = []
            for entry in name_list:
                new_path = os.path.join(current_directory, entry)
                if os.path.isfile(new_path):
                    files += _find_file_by_name(new_path, target_file)

            return files

        elif target_file == os.path.basename(current_path):
            return [os.path.abspath(current_path)]

    if os.path.isdir(current_path):
        files = []
        for file in os.listdir(current_path):
            files += _find_file_by_name(os.path.join(current_path, file), target_file)

        return files

    return []


def convert_to_records(path: str):
    text_id = os.path.basename(os.path.dirname(path)).upper()[:-4]

    with open(path, 'r') as file:
        json_data = json.load(file)

    full_text = str(json_data['_referenced_fss']['1']['sofaString'])
    annotations = json_data['_views']['_InitialView']['Span']
    sentence_data = json_data['_views']['_InitialView']['Sentence']

    len_annotations = len(annotations)

    sentence_records = []
    ground_truth_records = []
    value_records = []

    index_j = 0

    for i, entry in enumerate(sentence_data):
        sentence_id = i + 1
        start, end = entry.get('begin', 0), entry['end']
        unchanged_sentence = full_text[start:end]
        breakpoint_list = [
            match.start()for match in re.finditer('\\r\\n', unchanged_sentence)
        ]

        changed_sentence = unchanged_sentence.replace('\r\n', '\n')
        sentence_records.append({_text_id_ref: text_id, _sentence_id_ref: sentence_id, _text_ref: changed_sentence})

        ground_truth_record = {_text_id_ref: text_id, _sentence_id_ref: sentence_id}
        ground_truth_record.update({value: 'none' for value in _value_list})

        while index_j < len_annotations and start <= annotations[index_j].get('begin', 0) and annotations[index_j]['end'] <= end:
            value_start, value_end = annotations[index_j].get('begin', 0) - start, annotations[index_j]['end'] - start
            value_start_changed, value_end_changed = value_start, value_end
            for i, breakpoint in enumerate(breakpoint_list):
                if breakpoint < value_start:
                    value_start_changed = value_start - i - 1
                if breakpoint < value_end:
                    value_end_changed = value_end - i - 1
                if value_end < breakpoint:
                    break

            value_name = _value_dictionary.get(str(annotations[index_j]['label']).upper(), 'NaN')
            if value_name == 'NaN':
                print(f'Error on {text_id}-{sentence_id} {value_start}:{value_end}')
                continue
            if 'Attainment' in annotations[index_j].keys():
                attainment = str(annotations[index_j]['Attainment'])[:-2]
            else:
                attainment = 'Not sure, can’t decide'

            ground_truth_record[value_name] = attainment
            value_records.append(
                {_text_id_ref: text_id, _sentence_id_ref: sentence_id, _label_ref: value_name, _attainment_ref: attainment, 'Begin': value_start_changed, 'End': value_end_changed}
            )

            index_j += 1

        ground_truth_records.append(ground_truth_record)

    return sentence_records, ground_truth_records, value_records


def parse_args():
    parser = argparse.ArgumentParser(prog="convert_curation.py", description='Converter for curation files')

    parser.add_argument('-i', '--input-file', type=str, required=True, help='The input file (e.g., zip-Archive) that contains or is "CURATION_USER.json"')
    parser.add_argument('-o', '--output-dir', type=str, required=False, help='Directory for final tsv-files (default: same directory as for the input-file)')

    return parser.parse_args()


def main(input_file: str, output_dir: str):
    curation_files = _find_file_by_name(input_file, 'CURATION_USER.json')

    sentence_records, ground_truth_records, value_records = [], [], []

    for file in curation_files:
        try:
            new_sentence_records, new_ground_truth_records, new_value_records = convert_to_records(file)
            sentence_records += new_sentence_records
            ground_truth_records += new_ground_truth_records
            value_records += new_value_records
        except KeyError as e:
            print(file)
            sys.exit(e)

    pd.DataFrame.from_records(sentence_records).to_csv(
        os.path.join(output_dir, 'sentences.tsv'),
        header=True, index=False, sep='\t'
    )
    pd.DataFrame.from_records(ground_truth_records).to_csv(
        os.path.join(output_dir, 'ground_truth.tsv'),
        header=True, index=False, sep='\t'
    )
    pd.DataFrame.from_records(value_records).to_csv(
        os.path.join(output_dir, 'values.tsv'),
        header=True, index=False, sep='\t'
    )


if __name__ == '__main__':
    args = parse_args()
    if args.output_dir is None:
        output_dir = os.path.dirname(args.input_file)
    else:
        output_dir = args.output_dir
    main(input_file=args.input_file, output_dir=output_dir)
