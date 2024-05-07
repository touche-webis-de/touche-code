#!/usr/bin/env python3

import argparse
import copy
import json
from typing import Union, List, Optional, Dict

import sys
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
_attainment_ref = 'Attainment'
_time_stamp_ref = 'Time'

_value_list = ["Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance"]
_value_dictionary = {value.replace(':', ' -').upper(): value for value in _value_list}

######################
# END: CONSTANTS #####
######################


class NoSpanEntryError(KeyError):
    pass


########################
# START: Languages #####
########################

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

######################
# END: Languages #####
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


def convert_text_to_records(path: str, text_id: str):
    with open(path, 'r') as file:
        json_data = json.load(file)

    full_text = str(json_data['_referenced_fss']['1']['sofaString'])
    sentence_data = json_data['_views']['_InitialView']['Sentence']

    len_full_text = len(full_text)
    len_sentence_data = len(sentence_data)

    sentence_records = []
    sentence_id = 1
    for i, entry in enumerate(sentence_data):
        sentence_id = i + 1
        entry['begin'] = entry.get('begin', 0)
        entry['text'] = full_text[entry['begin']:entry['end']].replace('\r\n', '  ').replace('\n', ' ')\
            .replace(b'\xEF\xBB\xBF'.decode('utf-8'), ' ').replace('\r', ' ')

        sentence_records.append({
            _text_id_ref: text_id, _sentence_id_ref: sentence_id, _text_ref: entry['text'],
            'begin': entry['begin'], 'end': entry['end']
        })

    return sentence_records


def convert_to_records(path: str, text_id: str, text_df: pd.DataFrame, progress=None):
    with open(path, 'r') as file:
        json_data = json.load(file)

    if 'Span' not in json_data['_views']['_InitialView'].keys():
        raise NoSpanEntryError(f'Missing "Span" entry in {path}')

    annotations: List = json_data['_views']['_InitialView']['Span']
    annotations.sort(key=lambda x: (x.get('begin', 0), x['end']))

    annotation_records = []

    for i, annotation in enumerate(annotations):
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
                    print(f'Error on {text_id}-{row[_sentence_id_ref]} Curator :{text_range}')
                else:
                    progress.write(f'Error on {text_id}-{row[_sentence_id_ref]} Curator :{text_range}')
                break
            if 'Attainment' in annotation.keys():
                attainment = str(annotation['Attainment'])[:-2].strip()
            else:
                attainment = 'Not sure, can’t decide'

            # TODO Integrate Names and time stamps
            annotation_records.append({
                _text_id_ref: text_id, _sentence_id_ref: row[_sentence_id_ref], _coder_ref: 'Curator',
                _coded_text_ref: coded_text, _label_ref: value_name, _attainment_ref: attainment,
                _time_stamp_ref: 'Time'
            })

            index_loc += 1

    return annotation_records


############
# Main #####
############

def parse_args():
    parser = argparse.ArgumentParser(prog="convert_curation.py", description='Converter for curation files')

    parser.add_argument('-i', '--input-file', type=str, required=True, help='The input file (e.g., zip-Archive) that contains or is "CURATION_USER.json"')
    parser.add_argument('-o', '--output-dir', type=str, required=False, help='Directory for final tsv-files (default: same directory as for the input-file)')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='Whether to print intermediate info, e.g. values across sentence borders (default: False)')

    return parser.parse_args()


def main(input_file: str, output_dir: str, verbose: bool = False):
    curation_files = list(set(_find_file_by_name(input_file, 'CURATION_USER.json')))

    annotation_records = []
    # value_records = []

    batches = {}
    texts: Dict[str, List] = {}
    known_text_ids = []
    if verbose:
        print("==================================================\n"
              "Detecting present languages and collecting raw text\n"
              "==================================================")
    for file in tqdm(curation_files, desc='Files', disable=not verbose):
        # get text_id from file path
        text_id = os.path.basename(os.path.dirname(file)).upper()[:-4]
        language = _detect_language(text_id)
        if language is None:
            print(f'Unable to detect language for file "{text_id}".')
            continue
        if language in batches.keys():
            batches[language].append((text_id, file))
        else:
            batches[language] = [(text_id, file)]
        
        if text_id in known_text_ids:
            continue
        known_text_ids.append(text_id)

        new_sentence_records = convert_text_to_records(
            path=file, text_id=text_id
        )

        if language in texts.keys():
            texts[language] += new_sentence_records
        else:
            texts[language] = new_sentence_records

    texts: Dict[str, pd.DataFrame] = {key: pd.DataFrame.from_records(value) for key, value in texts.items()}

    for language, batch in batches.items():
        if verbose:
            print("==================================================\n"
                  f"Processing {len(batch)} files for {language}\n"
                  "==================================================")
        with tqdm(total=len(batch), desc=f'{language}', disable=not verbose) as progress:
            for text_id, file in batch:
                text_df = texts[language].loc[texts[language][_text_id_ref] == text_id, :]
                try:
                    new_annotation_records = \
                        convert_to_records(file, text_id, text_df, progress=progress if verbose else None)
                    annotation_records += new_annotation_records
                except NoSpanEntryError as nSEE:
                    progress.write(str(nSEE))
                except ValueError as vE:
                    progress.write(str(vE))
                except KeyError as e:
                    print(file)
                    raise e
                progress.update()

    texts_df = pd.concat(list(texts.values()), ignore_index=True).loc[:, [_text_id_ref, _sentence_id_ref, _text_ref]] \
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
    if args.output_dir is None:
        output_dir = os.path.dirname(args.input_file)
    else:
        output_dir = args.output_dir
    main(input_file=args.input_file, output_dir=output_dir, verbose=args.verbose)
