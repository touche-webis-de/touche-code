import nltk
import os
import pandas
import re
import sys

values = ["Self-direction", "Stimulation", "Hedonism", "Achievement", "Power", "Face", "Security", "Tradition", "Conformity", "Humility", "Benevolence", "Universalism"]
value_indices = {value.lower():index for index, value in enumerate(values)}
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
language = None
if len(sys.argv) > 3:
    language = sys.argv[3]

script_directory = os.path.dirname(os.path.realpath(__file__))
value_dicts = {}
def get_value_dict(language_tag):
    if language_tag not in value_dicts:
        print("Loading dict for " + language_tag)
        value_dict = {}
        value_dict_file_name = os.path.join(script_directory, "values-dict-" + language_tag.lower() + "-2022-10-07.tsv")
        if os.path.isfile(value_dict_file_name):
            value_dict_frame = pandas.read_csv(value_dict_file_name, sep='\t', header=0, index_col=None)
            for value, words in value_dict_frame.items():
                value_index = value_indices[value.lower()]
                for word in words:
                    if word == word:
                        # word != word tests for NaN
                        word_norm = word.lower()
                        if word_norm not in value_dict:
                            value_dict[word_norm] = [value_index]
                        else:
                            value_dict[word_norm].append(value_index)
        else:
            print("Failed to find dict for " + language_tag)
        value_dicts[language_tag] = value_dict
    return value_dicts[language_tag]

with open(output_file_name, "w") as output_file:
    output_file.write("\t".join(values) + "\n")
    for index, row in pandas.read_csv(input_file_name, sep='\t', header=0, index_col=None).iterrows():
        language_tag = language
        if language_tag == None:
            language_tag = re.sub(r'_.*', '', row["Text-ID"])
        value_dict = get_value_dict(language_tag)
        predictions = [0] * len(value_indices)
        if value_dict:
            tokens = nltk.tokenize.word_tokenize(row["Text"], language_tag, True)
            for token in tokens:
                token_norm = token.lower()
                if token_norm in value_dict:
                    for value_index in value_dict[token_norm]:
                        predictions[value_index] += (1 / len(tokens))
        output_file.write(row["Text-ID"] + "\t" + str(row["Sentence-ID"]))
        for prediction in predictions:
            output_file.write("\t%.2f" % prediction)
        output_file.write("\n")



