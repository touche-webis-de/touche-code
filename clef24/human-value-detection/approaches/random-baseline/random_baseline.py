import os
import pandas
import random
import sys

# SETUP

values = [ "Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance" ]

# PREDICTION

def predict(text):
    """ Predicts the value probabilities (attained and constrained) for each sentence """
    # "text" contains all sentences (plain strings) of a single text in order (same Text-ID in the input file)
    labels = []
    for sentence in text:
        sentence_labels = {}
        for value in values:
            # probability for subtask 1
            probability_resorted = random.random() 

            # randomly distribute probability between attained and constrained for subtask 2
            probability_attained = random.random() * probability_resorted
            probability_constrained = probability_resorted - probability_attained

            sentence_labels[value + " attained"] = probability_attained
            sentence_labels[value + " constrained"] = probability_constrained
        labels.append(sentence_labels)
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
    pandas.read_csv(input_file, sep='\t', header=0, index_col=None).groupby("Text-ID").apply(lambda text_instances:
        # label the instances of each text separately
        labeled_instances.extend(label(text_instances.sort_values("Sentence-ID").to_dict("records")))
    )
    writeRun(labeled_instances, output_dir)

