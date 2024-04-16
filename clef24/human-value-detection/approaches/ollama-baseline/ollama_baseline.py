import gzip
import json
import os
import ollama
import pandas
import random
import re
import sys
import threading

# SETUP

values = [ "Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance" ]

llm = ollama.Client(host="https://futuringmachines.webis.de")
model = "llama2"
prompt_subtask1_template = "Given the following SENTENCE, determine the degree (between 0 and 1) that the SENTENCE refers to the human value of {value}. Think step by step. Then say \"ANSWER: \" followed by your determined degree as single number between 0 and 1.\nSENTENCE: {sentence}\n"
prompt_subtask2_template = "Given the following SENTENCE, determine the degree (between 0 and 1) that the SENTENCE attains rather than constrains the human value of {value}. Think step by step. Then say \"ANSWER: \" followed by your determined degree as single number between 0 and 1.\nSENTENCE: {sentence}\n"

# CACHING
cache_file_name = "cache.json.gzip"

llm_cache = {}
if os.path.isfile(cache_file_name):
    with gzip.open(cache_file_name, "r") as cache_file:
        llm_cache = json.loads(cache_file.read().decode("utf-8"))

def cached_llm(model, prompt, force_upstream = False):
    if force_upstream or prompt not in llm_cache:
        response = llm.generate(model = model, prompt = prompt)
        llm_cache[prompt] = response
        return response
    else:
        return llm_cache[prompt]

mutex = threading.Lock()
def write_cache():
    with mutex:
        with gzip.open(cache_file_name, "w") as cache_file:
            cache_file.write(json.dumps(llm_cache).encode("utf-8"))

# PREDICTION

def ask_for_degree(prompt):
    answers = []
    repeated_try = False # allow cached response on first try
    while len(answers) == 0:
        response = cached_llm(model = model, prompt = prompt, force_upstream = repeated_try)
        answers = re.findall(r"ANSWER: [01]\.?[0-9]*", response["response"])
        print(answers)
        repeated_try = True
    return min(1.0, float(re.findall(r"[.0-9]+", answers[0])[0]))

def predict(text):
    """ Predicts the value probabilities (attained and constrained) for each sentence """
    # "text" contains all sentences (plain strings) of a single text in order (same Text-ID in the input file)
    labels = []
    for sentence in text:
        sentence_labels = {}
        for value in values:
            # probability for subtask 1
            prompt = prompt_subtask1_template.format(sentence = sentence, value = value)
            degree_resorted = ask_for_degree(prompt)

            # randomly distribute probability between attained and constrained for subtask 2
            prompt = prompt_subtask2_template.format(sentence = sentence, value = value)
            degree_attained = ask_for_degree(prompt) * degree_resorted
            degree_constrained = degree_resorted - degree_attained

            print(f"Got {degree_attained}/{degree_constrained} for \"{sentence}\" and {value}")

            sentence_labels[value + " attained"] = degree_attained
            sentence_labels[value + " constrained"] = degree_constrained
        labels.append(sentence_labels)
    write_cache() # store current cache
    return labels

# EXECUTION

def label(instances):
    """ Predicts the label probabilities for each instance and adds them to it """
    text = [instance["Text"] for instance in instances]
    return [{
            "Text-ID": instance["Text-ID"],
            "Sentence-ID": instance["Sentence-ID"],
            **labels
        } for instance, labels in zip(instances, predict(text))]

def writeRun(labeled_instances, output_dir):
    """ Writes all (labeled) instances to the predictions.tsv in the output directory """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "predictions.tsv")
    pandas.DataFrame.from_dict(labeled_instances).to_csv(output_file, header=True, index=False, sep='\t')

# code not executed by tira-run-inference-server (which directly calls 'predict(text)')
if "TIRA_INFERENCE_SERVER" not in os.environ:
    dataset_dir = sys.argv[1]
    output_dir = sys.argv[2]
    labeled_instances = []
    input_file = os.path.join(dataset_dir, "sentences.tsv")
    for text_instances in pandas.read_csv(input_file, sep='\t', header=0, index_col=None).groupby("Text-ID"):
        # label the instances of each text separately
        labeled_instances.extend(label(text_instances[1].sort_values("Sentence-ID").to_dict("records")))
    writeRun(labeled_instances, output_dir)

