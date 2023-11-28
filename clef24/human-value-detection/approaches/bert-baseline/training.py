import argparse
import sys
import os
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


from components.setup import (load_arguments_from_tsv, load_labels_from_tsv,
                              combine_columns, split_arguments)
from components.models_bert import (train_bert_model, load_tokenizer, get_available_values_by_subtask)


def parse_args():
    parser = argparse.ArgumentParser(prog='training.py', description="Train the BERT model on the sentences.")

    parser.add_argument(
        "-s", "--subtask", type=str, choices=['1', '2'], required=False, default='1',
        help="The respective subtask to train for (default: '1')")
    parser.add_argument(
        "-v", "--validate", action="store_true",
        help="Request evaluation after training (default: False)")

    return parser.parse_args()


def main(dataset_dir='/dataset/', model_dir='/models/', tokenizer_dir="bert-base-uncased", subtask: Literal['1', '2'] = '2', validate=False):

    # Check model directory
    if os.path.isfile(model_dir):
        print('The specified <model-dir> "%s" points to an existing file' % model_dir)
        sys.exit(2)
    if os.path.isdir(model_dir) and len(os.listdir(model_dir)) > 0:
        print('The specified <model-dir> "%s" already exists and contains files' % model_dir)
        decision = input('Do You still want to proceed? [y/n]\n').lower()
        if decision != 'y':
            sys.exit(-1)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    load_tokenizer(tokenizer_dir)

    argument_filepath = os.path.join(dataset_dir, 'sentences.tsv')

    if not os.path.isfile(argument_filepath):
        print('The required file "sentences.tsv" is not present in the dataset directory')
        sys.exit(2)

    # load arguments
    df_arguments = load_arguments_from_tsv(argument_filepath, default_usage='train')
    if len(df_arguments) < 1:
        print('There are no arguments in file "%s"' % argument_filepath)
        sys.exit(2)

    values = get_available_values_by_subtask(subtask=subtask)

    # format dataset
    label_filepath = os.path.join(dataset_dir, 'labels-ground_truth.tsv')
    if not os.path.isfile(label_filepath):
        print('The required file "labels-ground_truth.tsv" is not present in the core_data directory')
        sys.exit(2)
    # read labels from .tsv file
    df_labels = load_labels_from_tsv(label_filepath, label_order=values, subtask=subtask)
    # join arguments and labels
    df_full_level = combine_columns(df_arguments, df_labels)
    # split dataframe by usage
    df_train_all, df_valid_all, _ = split_arguments(df_full_level)

    if len(df_train_all) < 1:
        print('There are no arguments listed for training.')
        sys.exit()

    if validate and len(df_valid_all) < 1:
        print('There are no arguments listed for validation. Proceeding without validation.')
        validate = False

    print("===> Bert: Training...")
    if validate:
        bert_model_evaluation = train_bert_model(df_train_all,
                                                 os.path.join(model_dir, f'bert_train_subtask_{subtask}'),
                                                 values,
                                                 test_dataframe=df_valid_all)
        print("F1-Scores:")
        print(bert_model_evaluation['eval_f1-score'])
    else:
        train_bert_model(df_train_all, os.path.join(model_dir, f'bert_train_subtask_{subtask}'), values)


if __name__ == '__main__':
    args = parse_args()
    main(subtask=args.subtask, validate=args.validate)
