import os
import datasets
import pandas
import numpy
import torch
import sys
import transformers
import tempfile

# https://github.com/NielsRogge/Transformers-Tutorials/blob/master/BERT/Fine_tuning_BERT_(and_friends)_for_multi_label_text_classification.ipynb

# GENERIC

values = [ "Self-direction: thought", "Self-direction: action", "Stimulation",  "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance" ]
labels = sum([[value + " attained", value + " constrained"] for value in values], [])
id2label = {idx:label for idx, label in enumerate(labels)}
label2id = {label:idx for idx, label in enumerate(labels)} 


# tokenizer = transformers.AutoTokenizer.from_pretrained(pretrained_model)

def load_dataset(directory, tokenizer, load_labels=True):
    sentences_file_path = os.path.join(directory, "sentences.tsv")
    labels_file_path = os.path.join(directory, "labels.tsv")
    
    data_frame = pandas.read_csv(sentences_file_path, encoding="utf-8", sep="\t", header=0)
    encoded_sentences = tokenizer(data_frame["Text"], truncation=True)

    if load_labels and os.path.isfile(labels_file_path):
        labels_frame = pandas.read_csv(labels_file_path, encoding="utf-8", sep="\t", header=0)
        labels_frame = pandas.merge(data_frame, labels_frame, on=["Text-ID", "Sentence-ID"])
        labels_matrix = np.zeros((labels_frame.shape[0], len(labels)))
        for idx, label in enumerate(labels):
            if label in labels_frame.columns:
                labels_matrix[:, idx] = (labels_frame[label] >= 0.5).astype(int)
        encoded_sentences["labels"] = labels_matrix.tolist()

    encoded_sentences = datasets.Dataset.from_dict(encoded_sentences)
    return encoded_sentences, data_frame["Text-ID"], data_frame["Sentence-ID"]


def compute_metrics(eval_prediction):
    prediction_scores, label_scores = eval_prediction
    predictions = prediction_scores >= 0.5
    labels = label_scores >= 0.5

    f1_scores = {}
    for i in range(eval_prediction.shape[1]):
        predicted = predictions[:,i].sum()
        true = labels[:,i].sum()
        true_positives = numpy.logical_and(predictions[:,i], labels[:,i]).sum()
        precision = 0 if predicted == 0 else true_positives / predicted
        recall = 0 if true == 0 else true_positives / true
        f1_scores[i] = round(0 if precision + recall == 0 else 2 * (precision * recall) / (precision + recall), 2)
    f1_scores['avg-f1-score'] = round(numpy.mean(list(f1_scores.values())), 2)

    return {'f1-score': f1scores, 'marco-avg-f1score': f1scores['avg-f1-score']}


def train(training_dataset, validation_dataset, pretrained_model="bert-base-uncased", tokenizer = tokenizer, batch_size=8, num_train_epochs=20, learning_rate=2e-5, weight_decay=0.01):
    output_dir = tempfile.TemporaryDirectory()
    args = transformers.TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="steps",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_train_epochs,
        weight_decay=weight_decay,
        load_best_model_at_end=True,
        metric_for_best_model='marco-avg-f1score'
    )

    model = transformers.AutoModelForSequenceClassification.from_pretrained(
        pretrained_model, problem_type="multi_label_classification",
        num_labels=len(labels), id2label=id2label, label2id=label2id)
    if torch.cuda.is_availabled():
        model = model.to('cuda')

    trainer = transformers.Trainer(model, args,
        train_dataset=training_dataset, eval_dataset=validation_dataset,
        compute_metrics=compute_metrics, tokenizer=tokenizer)
    trainer.train()
    trainer.evaluate()

    return model



# SETUP


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

