#!/usr/bin/env python3

import argparse
import copy
import json
from typing import Union, List, Optional, Dict

import sys
import os

import zipfile
from trankit import Pipeline
from tqdm import tqdm

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


class NoSpanEntryError(KeyError):
    pass


################################
# START: Trankit Functions #####
################################

_lang_codes = {
    'BG': 'bulgarian',
    'DE': 'german',
    'EL': 'greek',
    'EN': 'english',
    'FR': 'french',
    'HE': 'hebrew',
    'IT': 'italian',
    'NL': 'dutch',
    'TR': 'turkish'
}
_lang_pipelines = {}


def _detect_language(text_id: str, verbose: bool = False) -> Optional[str]:
    for code, language in _lang_codes.items():
        if text_id.upper().startswith(code):
            if verbose:
                print(f'Detected language {language} for TEXT-ID {text_id}')
            return language
    if verbose:
        print(f'Unable to detect language for file "{text_id}".')
    return None


def _get_pipeline_for_file(text_id: str, verbose: bool = False) -> "tuple[Optional[Pipeline], str]":
    detected_language = _detect_language(text_id=text_id, verbose=verbose)
    if detected_language is None:
        return None, ""

    global _lang_pipelines
    if detected_language in _lang_pipelines.keys():
        pipeline = _lang_pipelines[detected_language]
        if pipeline._config.active_lang != detected_language:
            pipeline.set_active(detected_language)
    else:
        pipeline = Pipeline(lang=detected_language)
        _lang_pipelines[detected_language] = pipeline
    return pipeline, detected_language


def _compare_entries(entry_sentence: Dict, entry_trankit: Dict) -> Dict:
    if entry_sentence is None:
        return entry_trankit
    if entry_trankit is None:
        return entry_sentence
    if entry_trankit['begin'] < entry_sentence['begin']:
        return entry_trankit
    if entry_trankit['begin'] == entry_sentence['begin']:
        if '\n' in entry_sentence['text']:
            return entry_trankit
        if entry_sentence['end'] - entry_sentence['begin'] <= 0.20 * (entry_trankit['end'] - entry_trankit['begin']):
            return entry_trankit
    return entry_sentence

##############################
# END: Trankit Functions #####
##############################


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


def convert_to_records(path: str, pipeline: Pipeline = None, verbose: bool = False, progress=None):
    text_id = os.path.basename(os.path.dirname(path)).upper()[:-4]

    with open(path, 'r') as file:
        json_data = json.load(file)

    full_text = str(json_data['_referenced_fss']['1']['sofaString'])
    if 'Span' not in json_data['_views']['_InitialView'].keys():
        annotations = []
        if progress is None:
            print(f'Missing "Span" entry in {path}')
        else:
            progress.write(f'Missing "Span" entry in {path}')
    else:
        annotations: List = json_data['_views']['_InitialView']['Span']
        annotations.sort(key=lambda x: (x.get('begin', 0), x['end']))
    sentence_data = json_data['_views']['_InitialView']['Sentence']

    len_full_text = len(full_text)
    len_sentence_data = len(sentence_data)
    len_annotations = len(annotations)

    sentence_records = []
    ground_truth_records = []
    ground_truth_label_records = []
    # value_records = []

    if pipeline is None:
        trankit_pipeline, _ = _get_pipeline_for_file(text_id)
    else:
        trankit_pipeline = pipeline
    sentence_data_trankit = []
    if trankit_pipeline is not None:
        sentence_data_trankit = [
            {'text': sentence_dict['text'], 'begin': sentence_dict['dspan'][0], 'end': sentence_dict['dspan'][1], 'trankit': True}
            for sentence_dict in trankit_pipeline.ssplit(full_text)['sentences']
        ]
    len_sentence_data_trankit = len(sentence_data_trankit)

    index_full_text = 0
    index_sentence = 0
    index_trankit_sentence = 0

    sentence_id = 1
    while index_full_text < len_full_text:
        # select next valid sentence entry
        while index_sentence < len_sentence_data and sentence_data[index_sentence].get('begin', 0) < index_full_text:
            index_sentence += 1
        entry_sentence = None
        if index_sentence < len_sentence_data:
            entry_sentence = sentence_data[index_sentence]
            entry_sentence['begin'] = entry_sentence.get('begin', 0)
            entry_sentence['text'] = full_text[entry_sentence['begin']:entry_sentence['end']]

        # select next valid trankit entry
        while index_trankit_sentence < len_sentence_data_trankit and sentence_data_trankit[index_trankit_sentence]['begin'] < index_full_text:
            index_trankit_sentence += 1
        entry_trankit = None
        if index_trankit_sentence < len_sentence_data_trankit:
            entry_trankit = sentence_data_trankit[index_trankit_sentence]

        # select matching entry
        selected_entry = _compare_entries(entry_sentence, entry_trankit)
        if selected_entry is None:
            if len(full_text[index_full_text:].strip()) > 0:
                raise ValueError(f'No valid sentence for document "{path}" past index {index_full_text}.')
            else:
                break

        # prepare records
        sentence_text = selected_entry['text'].replace('\r\n', '  ').replace('\n', ' ')\
            .replace('<feff>', '      ')
        if '^M' in sentence_text:
            sentence_text_parts = str(sentence_text).split('^M')
            sentence_start_end_list = [(selected_entry['begin'], len(sentence_text_parts[0]))]
            next_start = sentence_start_end_list[0][1] + 2
            for i in range(1, len(sentence_text_parts) - 1):
                next_end = next_start + len(sentence_text_parts[i])
                sentence_start_end_list.append((next_start, next_end))
                next_start = next_end + 2
            sentence_start_end_list.append((next_start, selected_entry['end']))
        else:
            sentence_text_parts = [sentence_text]
            sentence_start_end_list = [(selected_entry['begin'], selected_entry['end'])]

        for i, uncleaned_sentence_text in enumerate(sentence_text_parts):
            # remove repetitive spaces
            while '  ' in uncleaned_sentence_text:
                uncleaned_sentence_text = uncleaned_sentence_text.replace('  ', ' ')

            sentence_text = uncleaned_sentence_text
            sentence_records.append({_text_id_ref: text_id, _sentence_id_ref: sentence_id, _text_ref: sentence_text})
            ground_truth_record = {_text_id_ref: text_id, _sentence_id_ref: sentence_id}
            ground_truth_record.update({value: 'none' for value in _value_list})
            sentence_start_end = sentence_start_end_list[i]

            # Process annotations
            annotations_index = 0
            while annotations and annotations_index < len(annotations):
                if 'overlap' in annotations[annotations_index].keys() and \
                        sentence_start_end[0] > annotations[annotations_index].get('begin', 0):
                    annotations[annotations_index]['begin'] = sentence_start_end[0]
                if not (sentence_start_end[0] <= annotations[annotations_index].get('begin', 0) < sentence_start_end[1]):
                    annotations_index += 1
                    continue
                annotation = annotations.pop(annotations_index)
                annotations_index -= 1

                # Apply overlapping value to all touched sentences
                if annotation['end'] > sentence_start_end[1]:
                    if verbose:
                        if 'trankit' in selected_entry.keys():
                            if progress is None:
                                print(f"Value \"{annotation}\" across sentence borders (due to trankit) for file \"{path}\"")
                            else:
                                progress.write(f"Value \"{annotation}\" across sentence borders (due to trankit) for file \"{path}\"")
                        else:
                            if progress is None:
                                print(f"Value \"{annotation}\" across sentence borders for file \"{path}\"")
                            else:
                                progress.write(f"Value \"{annotation}\" across sentence borders for file \"{path}\"")
                    new_annotation = copy.deepcopy(annotation)
                    new_annotation['overlap'] = True
                    new_annotation['begin'] = sentence_start_end[1]
                    annotation['end'] = sentence_start_end[1]
                    annotations.insert(0, new_annotation)
                    annotations_index += 1

                value_start = annotation.get('begin', 0) - sentence_start_end[0]
                value_end = annotation['end'] - sentence_start_end[0]

                value_name = _value_dictionary.get(str(annotation['label']).upper(), 'NaN')
                if value_name == 'NaN':
                    if progress is None:
                        print(f'Error on {text_id}-{sentence_id} {value_start}:{value_end}')
                    else:
                        progress.write(f'Error on {text_id}-{sentence_id} {value_start}:{value_end}')
                    continue
                if 'Attainment' in annotation.keys():
                    attainment = str(annotation['Attainment'])[:-2].strip()
                else:
                    attainment = 'Not sure, can’t decide'

                ground_truth_record[value_name] = attainment
                # value_records.append(
                #     {_text_id_ref: text_id, _sentence_id_ref: sentence_id, _label_ref: value_name,
                #      _attainment_ref: attainment, 'Begin': value_start, 'End': value_end}
                # )

                annotations_index += 1

            # pre-sort annotations for next sentence
            annotations.sort(key=lambda x: (x.get('begin', 0), x['end']))

            ground_truth_records.append(ground_truth_record)
            ground_truth_label_record = {_text_id_ref: text_id, _sentence_id_ref: sentence_id}
            for value_name in _value_list:
                confidence_attained = 0.0
                confidence_constrained = 0.0
                if ground_truth_record[value_name] == '(Partially) attained':
                    confidence_attained = 1.0
                elif ground_truth_record[value_name] == '(Partially) constrained':
                    confidence_constrained = 1.0
                elif ground_truth_record[value_name] == 'Not sure, can’t decide':
                    confidence_attained = 0.5
                    confidence_constrained = 0.5
                ground_truth_label_record[value_name + " attained"] = confidence_attained
                ground_truth_label_record[value_name + " constrained"] = confidence_constrained
            ground_truth_label_records.append(ground_truth_label_record)

            sentence_id += 1
            index_full_text = sentence_start_end[1]

    return sentence_records, ground_truth_records, ground_truth_label_records  # , value_records


def parse_args():
    parser = argparse.ArgumentParser(prog="convert_curation.py", description='Converter for curation files')

    parser.add_argument('-i', '--input-file', type=str, required=True, help='The input file (e.g., zip-Archive) that contains or is "CURATION_USER.json"')
    parser.add_argument('-o', '--output-dir', type=str, required=False, help='Directory for final tsv-files (default: same directory as for the input-file)')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Whether to print intermediate info, e.g. values across sentence borders (default: False)')

    return parser.parse_args()


def main(input_file: str, output_dir: str, verbose: bool = False):
    curation_files = _find_file_by_name(input_file, 'CURATION_USER.json')

    sentence_records, ground_truth_records, ground_truth_label_records = [], [], []
    # value_records = []

    batches = {}

    print("==================================================\n"
          "Detecting present languages\n"
          "==================================================")
    for file in curation_files:
        # get text_id from file path
        text_id = os.path.basename(os.path.dirname(file)).upper()[:-4]

        language = _detect_language(text_id)
        if language is not None:
            if language in batches.keys():
                batches[language].append((text_id, file))
            else:
                batches[language] = [(text_id, file)]
        else:
            print(f'Unable to detect language for file "{text_id}".')

    for language, batch in batches.items():
        print("==================================================\n"
              f"Processing {len(batch)} files for {language}\n"
              "==================================================")
        pipeline, _ = _get_pipeline_for_file(batch[0][0])
        with tqdm(total=len(batch), desc=f'{language}', disable=False) as progress:
            for text_id, file in batch:
                try:
                    new_sentence_records, new_ground_truth_records, new_ground_truth_label_records = \
                        convert_to_records(file, pipeline=pipeline, verbose=verbose, progress=progress)
                    sentence_records += new_sentence_records
                    ground_truth_records += new_ground_truth_records
                    ground_truth_label_records += new_ground_truth_label_records
                    # value_records += new_value_records
                except NoSpanEntryError as nSEE:
                    progress.write(str(nSEE))
                except ValueError as vE:
                    progress.write(str(vE))
                except KeyError as e:
                    print(file)
                    raise e
                progress.update()

    pd.DataFrame.from_records(sentence_records).sort_values(by=[_text_id_ref, _sentence_id_ref]).to_csv(
        os.path.join(output_dir, 'sentences.tsv'),
        header=True, index=False, sep='\t'
    )
    pd.DataFrame.from_records(ground_truth_records).sort_values(by=[_text_id_ref, _sentence_id_ref]).to_csv(
        os.path.join(output_dir, 'ground_truth.tsv'),
        header=True, index=False, sep='\t'
    )
    pd.DataFrame.from_records(ground_truth_label_records).sort_values(by=[_text_id_ref, _sentence_id_ref]).to_csv(
        os.path.join(output_dir, 'labels-ground_truth.tsv'),
        header=True, index=False, sep='\t'
    )
    # pd.DataFrame.from_records(value_records).sort_values(by=[_text_id_ref, _sentence_id_ref, 'Begin']).to_csv(
    #     os.path.join(output_dir, 'values.tsv'),
    #     header=True, index=False, sep='\t'
    # )


if __name__ == '__main__':
    args = parse_args()
    if args.output_dir is None:
        output_dir = os.path.dirname(args.input_file)
    else:
        output_dir = args.output_dir
    main(input_file=args.input_file, output_dir=output_dir, verbose=args.verbose)
