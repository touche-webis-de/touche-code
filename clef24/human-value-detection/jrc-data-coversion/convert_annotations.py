#!/usr/bin/env python3

import argparse
import json
from datetime import datetime
from typing import List, Dict

import os
import re

import zipfile
from tqdm import tqdm

import pandas as pd

########################
# START: CONSTANTS #####
########################

_text_id_ref = 'Text-ID'
_sentence_id_ref = 'Segment'
_text_ref = 'Text'
_coder_ref = 'Coder'
_coded_text_ref = 'Coded-Text'
_label_ref = 'Value'
_coarse_label_ref = 'Coarse-Value'
_attainment_ref = 'Attainment'
_time_stamp_ref = 'Time'
_index_ref = 'Index'
_length_ref = 'Length'

_value_list = ["Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement",
               "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition",
               "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring",
               "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance"]

_coarse_value_mapping = {
    "Self-direction: thought": "Self-direction",
    "Self-direction: action": "Self-direction",
    "Stimulation": "Stimulation",
    "Hedonism": "Hedonism",
    "Achievement": "Achievement",
    "Power: dominance": "Power",
    "Power: resources": "Power",
    "Face": "Power",
    "Security: personal": "Security",
    "Security: societal": "Security",
    "Tradition": "Tradition",
    "Conformity: rules": "Conformity",
    "Conformity: interpersonal": "Conformity",
    "Humility": "Conformity",
    "Benevolence: caring": "Benevolence",
    "Benevolence: dependability": "Benevolence",
    "Universalism: concern": "Universalism",
    "Universalism: nature": "Universalism",
    "Universalism: tolerance": "Universalism"
}

_value_dictionary = {value.replace(':', ' -').upper(): value for value in _value_list}

_languages = ['bulgarian', 'german', 'greek', 'english', 'french', 'hebrew', 'italian', 'dutch', 'turkish']


######################
# END: CONSTANTS #####
######################


class NoSpanEntryError(KeyError):

    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


def _find_file_by_name(current_path: str, target_file: str, skip_zip: bool = False) -> List[str]:
    if os.path.isfile(current_path):

        if current_path.endswith('.zip'):
            current_directory = current_path[:current_path.rindex('.')]
            if not os.path.isdir(current_directory):
                os.makedirs(current_directory)

            with zipfile.ZipFile(current_path, 'r') as zip_arc:
                name_list = zip_arc.namelist()
                if not skip_zip:
                    zip_arc.extractall(current_directory)

            files = []
            for entry in name_list:
                new_path = os.path.join(current_directory, entry)
                if os.path.isfile(new_path):
                    files += _find_file_by_name(new_path, target_file, skip_zip=skip_zip)

            return files

        elif target_file == os.path.basename(current_path):
            return [os.path.abspath(current_path)]

    if os.path.isdir(current_path):
        files = []
        for file in os.listdir(current_path):
            files += _find_file_by_name(os.path.join(current_path, file), target_file, skip_zip=skip_zip)

        return files

    return []


def parse_project_file(path: str, anon_mapping: Dict[str, str]):
    with open(path, 'r') as file:
        json_dict = json.load(file)

    name = json_dict["name"]

    sentence_records = []

    full_text_mapping = {}

    for source_document in json_dict["source_documents"]:
        if source_document["state"] not in ["CURATION_FINISHED", "CURATION_IN_PROGRESS"]:
            continue

        text_id = source_document['name']

        initial_cas_file = os.path.join(os.path.dirname(path), f"annotation/{text_id}/INITIAL_CAS/INITIAL_CAS.json")

        new_sentence_records, cleaned_full_text, length_difference = convert_text_to_records(initial_cas_file, text_id)
        sentence_records += new_sentence_records

        full_text_mapping[text_id] = (cleaned_full_text, length_difference)

    language_batch = []

    for annotation_documents in json_dict["annotation_documents"]:

        if annotation_documents["state"] != "FINISHED" or annotation_documents["annotatorState"] != "FINISHED":
            continue

        text_id = annotation_documents["name"]

        user = annotation_documents["user"]
        user_anon = anon_mapping[user]

        annotation_file = os.path.join(os.path.dirname(path), f"annotation/{text_id}/{user}/{user}.json")

        time = datetime.fromtimestamp(int(annotation_documents["timestamp"]) / 1000.0).isoformat(' ', timespec='seconds')

        language_batch.append((text_id, annotation_file, user_anon, time))

    return name, sentence_records, language_batch, full_text_mapping


def convert_text_to_records(path: str, text_id: str):
    with open(path, 'r') as file:
        json_data = json.load(file)

    full_text = str(json_data['_referenced_fss']['1']['sofaString'])
    sentence_data = json_data['_views']['_InitialView']['Sentence']

    cleaned_full_text = re.sub(r' [ ]+', ' ', full_text.replace('\r\n', '  ').replace('\n', ' ')
                               .replace(b'\xEF\xBB\xBF'.decode('utf-8'), ' ').replace('\r', ' '))
    length_difference = len(full_text) - len(cleaned_full_text)

    sentence_records = []
    for i, entry in enumerate(sentence_data):
        sentence_id = i + 1
        entry['begin'] = entry.get('begin', 0)
        entry['text'] = full_text[entry['begin']:entry['end']].replace('\r\n', '  ').replace('\n', ' ') \
            .replace(b'\xEF\xBB\xBF'.decode('utf-8'), ' ').replace('\r', ' ')

        cleaned_text = re.sub(r' [ ]+', ' ', entry['text'])
        sentence_index = cleaned_full_text.find(cleaned_text, max(entry['begin'] - length_difference, 0))
        sentence_length = len(cleaned_text)

        sentence_records.append({
            _text_id_ref: text_id, _sentence_id_ref: sentence_id, _text_ref: entry['text'],
            'begin': entry['begin'], 'end': entry['end'],
            _index_ref: sentence_index, _length_ref: sentence_length
        })

    return sentence_records, cleaned_full_text, length_difference


def convert_to_records(
        path: str,
        text_id: str,
        text_df: pd.DataFrame,
        user_anon: str,
        time: str,
        cleaned_text: str,
        length_difference: int,
        progress=None):
    with open(path, 'r') as file:
        json_data = json.load(file)

    if 'Span' not in json_data['_views']['_InitialView'].keys():
        raise NoSpanEntryError(f'Missing "Span" entry in {text_id} User: {user_anon}')

    annotations: List = json_data['_views']['_InitialView']['Span']
    annotations.sort(key=lambda x: (x.get('begin', 0), x['end']))

    annotation_records = []

    for i, annotation in enumerate(annotations):
        if "label" not in annotation.keys():
            if progress is None:
                print(f'Missing label for annotation on {text_id} User: {user_anon}')
            else:
                progress.write(f'Missing label for annotation on {text_id} User: {user_anon}')
            continue
        start: int = annotation.get('begin', 0)
        end: int = annotation['end']

        filter_index: pd.Series = (text_df.begin <= start)
        index_loc = filter_index.where(filter_index).last_valid_index()
        if index_loc is None:
            raise KeyError

        while index_loc < len(text_df) and end > text_df.iloc[index_loc].begin:
            row = text_df.iloc[index_loc]
            raw_text = row[_text_ref]
            text_range = max(start - row.begin, 0), min(end - row.begin, len(raw_text))
            coded_text = re.sub(r' [ ]+', ' ', raw_text[text_range[0]:text_range[1]])

            value_name = _value_dictionary.get(str(annotation['label']).upper(), 'NaN')
            if value_name == 'NaN':
                if progress is None:
                    print(f'Error on {text_id}-{row[_sentence_id_ref]} User: {user_anon}')
                else:
                    progress.write(f'Error on {text_id}-{row[_sentence_id_ref]} User: {user_anon}')
                break
            if 'Attainment' in annotation.keys():
                attainment = str(annotation['Attainment'])[:-2].strip()
            else:
                attainment = 'Not sure, can’t decide'

            annotation_index = cleaned_text.find(coded_text, max(text_range[0] - length_difference, 0))
            annotation_length = len(coded_text)

            annotation_records.append({
                _text_id_ref: text_id, _sentence_id_ref: row[_sentence_id_ref], _coder_ref: user_anon,
                _coded_text_ref: coded_text, _index_ref: annotation_index, _length_ref: annotation_length,
                _label_ref: value_name, _coarse_label_ref: _coarse_value_mapping[value_name],
                _attainment_ref: attainment, _time_stamp_ref: time
            })

            index_loc += 1

    return annotation_records


############
# Main #####
############

def parse_args():
    parser = argparse.ArgumentParser(prog="convert_curation.py", description='Converter for curation files')

    parser.add_argument('-i', '--input-file', type=str, required=True,
                        help='The input file (e.g., zip-Archive) that contains "exportedproject.json" together with the annotation files')
    parser.add_argument('-m', '--mapping', type=str, required=True,
                        help='The anonymity mapping for the annotation users')
    parser.add_argument('-o', '--output-dir', type=str, required=False,
                        help='Directory for final tsv-files (default: same directory as for the input-file)')
    parser.add_argument('-s', '--skip-unzipping', action='store_true', dest="zip",
                        help='Whether to skip the unzipping stage (time save, if archive is already unzipped) (default: False)')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Whether to print intermediate info, e.g. values across sentence borders (default: False)')

    return parser.parse_args()


def main(input_file: str, mapping_file: str, output_dir: str, skip_zip: bool = False, verbose: bool = False):
    project_files = list(set(_find_file_by_name(input_file, 'exportedproject.json', skip_zip=skip_zip)))

    with open(mapping_file, 'r') as file:
        anon_mapping = json.load(file)

    annotation_records = []

    batches = {}
    texts: Dict[str, pd.DataFrame] = {}
    full_text = {}

    if verbose:
        print("==================================================\n"
              "Detecting present languages and collecting raw text\n"
              "==================================================")
    for file in tqdm(project_files, desc='Archives', disable=not verbose):
        # get text_id from file path
        language = None
        for known_language in _languages:
            if known_language in file:
                language = known_language
                break

        if language is None:
            print(f'Unable to detect language for file "{file}".')
            continue

        name, sentence_records, language_batch, full_text_mapping = parse_project_file(file, anon_mapping)
        full_text.update(full_text_mapping)

        texts[name] = pd.DataFrame.from_records(sentence_records)

        batches[name] = language_batch

    for language, batch in batches.items():
        if verbose:
            print("==================================================\n"
                  f"Processing {len(batch)} files for {language}\n"
                  "==================================================")
        with tqdm(total=len(batch), desc=f'{language}', disable=not verbose) as progress:
            for text_id, file, user_anon, time in batch:
                cleaned_text, length_difference = full_text[text_id]
                text_df = texts[language].loc[texts[language][_text_id_ref] == text_id, :].reset_index(drop=True)
                try:
                    new_annotation_records = \
                        convert_to_records(file, text_id, text_df, user_anon, time,
                                           cleaned_text, length_difference,
                                           progress=progress if verbose else None)
                    annotation_records += new_annotation_records
                except NoSpanEntryError as nSEE:
                    if not verbose:
                        print(str(nSEE))
                    else:
                        progress.write(str(nSEE))
                except ValueError as vE:
                    if not verbose:
                        print(str(nSEE))
                    else:
                        progress.write(str(vE))
                except KeyError as e:
                    print(file)
                    raise e
                progress.update()

    texts_df = pd.concat(list(texts.values()), ignore_index=True).loc[:, [_text_id_ref, _sentence_id_ref, _text_ref, _index_ref, _length_ref]] \
        .drop_duplicates(subset=[_text_id_ref, _sentence_id_ref])
    # clean actual text
    texts_df[_text_ref] = texts_df[_text_ref].str.replace(r' [ ]+', ' ', regex=True).str.strip()
    texts_df \
        .sort_values(by=[_text_id_ref, _sentence_id_ref]).to_csv(
            os.path.join(output_dir, 'texts.tsv'),
            header=True, index=False, sep='\t'
        )

    pd.DataFrame.from_records(annotation_records) \
        .sort_values(by=[_text_id_ref, _sentence_id_ref, _coder_ref]).to_csv(
            os.path.join(output_dir, 'codes.tsv'),
            header=True, index=False, sep='\t'
        )


if __name__ == '__main__':
    args = parse_args()
    input_file = os.path.abspath(args.input_file)
    if args.output_dir is None:
        output_dir = os.path.dirname(input_file)
    else:
        output_dir = os.path.abspath(args.output_dir)
    main(input_file=input_file, mapping_file=args.mapping, output_dir=output_dir, skip_zip=args.zip,
         verbose=args.verbose)
