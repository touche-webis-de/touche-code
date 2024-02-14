import os
import pandas
import numpy
import torch
import sys
import transformers
import tempfile

# GENERIC

class MultiLabelTrainer(transformers.Trainer):
    """
        A transformers `Trainer` with custom loss computation

        Methods
        -------
        compute_loss(model, inputs, return_outputs=False):
            Overrides loss computation from Trainer class
        """
    def compute_loss(self, model, inputs, return_outputs=False):
        """Custom loss computation"""
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fct = torch.nn.BCEWithLogitsLoss()
        loss = loss_fct(logits.view(-1, self.model.config.num_labels),
                        labels.float().view(-1, self.model.config.num_labels))
        return (loss, outputs) if return_outputs else loss

def compute_metrics(eval_prediction, value_classes):
    """Custom metric calculation function for MultiLabelTrainer"""
    prediction_scores, label_scores = eval_prediction
    predictions = prediction_scores >= 0.5
    labels = label_scores >= 0.5

    f1_scores = {}
    for i, v in enumerate(value_classes):
        predicted = predictions.sum()
        true = labels.sum()
        true_positives = numpy.logical_and(predictions, labels).sum()
        precision = 0 if predicted == 0 else true_positives / predicted
        recall = 0 if true == 0 else true_positives / true
        f1_scores[v] = round(0 if precision + recall == 0 else 2 * (precision * recall) / (precision + recall), 2)
    f1_scores['avg-f1-score'] = round(numpy.mean(list(f1_scores.values())), 2)

    return {'f1-score': f1scores, 'marco-avg-f1score': f1scores['avg-f1-score']}

def train(batch_size=8, num_train_epochs=20):
    """Train a model"""
    output_dir = tempfile.TemporaryDirectory()
    args = transformers.TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="steps",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=num_train_epochs,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model='marco-avg-f1score'
    )



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

