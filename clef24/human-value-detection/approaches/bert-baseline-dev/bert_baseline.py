import datasets
import numpy
import os
import pandas
import sys
import tempfile
import torch
import transformers

# https://github.com/NielsRogge/Transformers-Tutorials/blob/master/BERT/Fine_tuning_BERT_(and_friends)_for_multi_label_text_classification.ipynb

# GENERIC

values = [ "Self-direction: thought", "Self-direction: action", "Stimulation",  "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance" ]
labels = sum([[value + " attained", value + " constrained"] for value in values], [])
id2label = {idx:label for idx, label in enumerate(labels)}
label2id = {label:idx for idx, label in enumerate(labels)} 

model_name = "JohannesKiesel/valueeval24-bert-baseline-toy-2024-02-27"

def load_dataset(directory, tokenizer, load_labels=True):
    sentences_file_path = os.path.join(directory, "sentences.tsv")
    labels_file_path = os.path.join(directory, "labels.tsv")
    
    data_frame = pandas.read_csv(sentences_file_path, encoding="utf-8", sep="\t", header=0)
    encoded_sentences = tokenizer(data_frame["Text"].to_list(), truncation=True)

    if load_labels and os.path.isfile(labels_file_path):
        labels_frame = pandas.read_csv(labels_file_path, encoding="utf-8", sep="\t", header=0)
        labels_frame = pandas.merge(data_frame, labels_frame, on=["Text-ID", "Sentence-ID"])
        labels_matrix = numpy.zeros((labels_frame.shape[0], len(labels)))
        for idx, label in enumerate(labels):
            if label in labels_frame.columns:
                labels_matrix[:, idx] = (labels_frame[label] >= 0.5).astype(int)
        encoded_sentences["labels"] = labels_matrix.tolist()

    encoded_sentences = datasets.Dataset.from_dict(encoded_sentences)
    return encoded_sentences, data_frame["Text-ID"].to_list(), data_frame["Sentence-ID"].to_list()


def compute_metrics(eval_prediction):
    prediction_scores, label_scores = eval_prediction
    predictions = prediction_scores >= 0.0 # sigmoid
    labels = label_scores >= 0.5

    f1_scores = {}
    for i in range(predictions.shape[1]):
        predicted = predictions[:,i].sum()
        true = labels[:,i].sum()
        true_positives = numpy.logical_and(predictions[:,i], labels[:,i]).sum()
        precision = 0 if predicted == 0 else true_positives / predicted
        recall = 0 if true == 0 else true_positives / true
        f1_scores[i] = round(0 if precision + recall == 0 else 2 * (precision * recall) / (precision + recall), 2)
    macro_average_f1_score = round(numpy.mean(list(f1_scores.values())), 2)

    return {'f1-score': f1_scores, 'marco-avg-f1-score': macro_average_f1_score}


def train(training_dataset, validation_dataset, pretrained_model, tokenizer, batch_size=8, num_train_epochs=20, learning_rate=2e-5, weight_decay=0.01):
    output_dir = tempfile.TemporaryDirectory()
    args = transformers.TrainingArguments(
        output_dir=output_dir.name,
        hub_model_id=model_name,
        evaluation_strategy="steps",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_train_epochs,
        weight_decay=weight_decay,
        load_best_model_at_end=True,
        metric_for_best_model='marco-avg-f1-score'
    )

    model = transformers.AutoModelForSequenceClassification.from_pretrained(
        pretrained_model, problem_type="multi_label_classification",
        num_labels=len(labels), id2label=id2label, label2id=label2id)
    if torch.cuda.is_available():
        model = model.to('cuda')

    print("\n\nTRAINING")
    print("========")
    trainer = transformers.Trainer(model, args,
        train_dataset=training_dataset, eval_dataset=validation_dataset,
        compute_metrics=compute_metrics, tokenizer=tokenizer)
    trainer.train()

    print("\n\nVALIDATION")
    print("==========")
    evaluation = trainer.evaluate()
    for idx, label in enumerate(labels):
        sys.stdout.write("%-39s %.2f\n" % (label + ":", evaluation["eval_f1-score"][idx]))
    sys.stdout.write("\n%-39s %.2f\n" % ("Macro average:", evaluation["eval_marco-avg-f1-score"]))

    print("\n\nUPLOAD")
    print("======")
    trainer.push_to_hub()

    return model




pretrained_model = "bert-base-uncased"
tokenizer = transformers.AutoTokenizer.from_pretrained(pretrained_model)
training_dataset, training_text_ids, training_sentence_ids = load_dataset(sys.argv[1], tokenizer)
validation_dataset, validation_text_ids, validation_sentence_ids = load_dataset(sys.argv[2], tokenizer)
model = train(training_dataset, validation_dataset, pretrained_model, tokenizer)

