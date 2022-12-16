import sys
import getopt
import os
import pandas as pd

from components.setup import (load_values_from_json, load_arguments_from_tsv, split_arguments,
                              write_tsv_dataframe, create_dataframe_head)
from components.models_bert import (predict_bert_model, load_tokenizer)

help_string = '\nUsage:  predict.py [OPTIONS]' \
              '\n' \
              '\nRequest prediction of the BERT model for all test arguments' \
              '\n' \
              '\nOptions:' \
              '\n  -h, --help               Display help text' \
              '\n  -i, --inputDataset       Directory with \'arguments.tsv\' file' \
              '\n  -l, --levels string      Comma-separated list of taxonomy levels to train models for (default "2")' \
              '\n  -o, --outputDir          Directory for writing the \'predictions.tsv\' file to'


def main(argv):
    data_dir = '/app/data/'
    dataset_dir = None
    model_dir = '/app/models/'
    tokenizer_dir = "/app/tokenizer"
    output_dir = None
    # default values
    levels = ["2"]

    try:
        opts, args = getopt.gnu_getopt(argv, "hi:l:o:", ["help", "inputDataset=", "levels=", "outputDir="])
    except getopt.GetoptError:
        print(help_string)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_string)
            sys.exit()
        elif opt in ('-l', '--levels'):
            levels = arg.split(",")
        elif opt in ('-i', '--inputDataset'):
            dataset_dir = arg
        elif opt in ('-o', '--outputDir'):
            output_dir = arg

    load_tokenizer(tokenizer_dir)

    argument_filepath = os.path.join(dataset_dir, 'arguments.tsv')
    values_filepath = os.path.join(data_dir, 'values.json')

    if not os.path.isfile(argument_filepath):
        print('The required file "arguments.tsv" is not present in the dataset directory')
        sys.exit(2)
    if not os.path.exists(output_dir):
        print('The specified output directory does not exist')
        sys.exit(2)

    # load arguments
    df_arguments = load_arguments_from_tsv(argument_filepath)
    if len(df_arguments) < 1:
        print('There are no arguments in file "%s"' % argument_filepath)
        sys.exit(2)

    values = load_values_from_json(values_filepath)
    num_levels = len(levels)

    # check levels
    for i in range(num_levels):
        if levels[i] not in values:
            print('Missing attribute "{}" in value.json'.format(levels[i]))
            sys.exit(2)

    # check model directory
    if not os.path.isdir(model_dir):
        print('The specified <model-dir> "%s" does not exist' % model_dir)
        sys.exit(2)

    for i in range(num_levels):
        if not os.path.exists(os.path.join(model_dir, 'bert_train_level{}'.format(levels[i]))):
            print('Missing saved Bert model for level "{}"'.format(levels[i]))
            sys.exit(2)

    # format dataset
    _, _, df_test = split_arguments(df_arguments)

    if len(df_test) < 1:
        print('There are no arguments listed for prediction.')
        sys.exit()

    # predict with Bert model
    df_prediction = create_dataframe_head(df_test['Argument ID'])
    for i in range(num_levels):
        print("===> Bert: Predicting Level %s..." % levels[i])
        result = predict_bert_model(df_test, os.path.join(model_dir, 'bert_train_level{}'.format(levels[i])),
                                    values[levels[i]])
        df_prediction = pd.concat([df_prediction, pd.DataFrame(result, columns=values[levels[i]])], axis=1)

    # write predictions
    print("===> Writing predictions...")
    write_tsv_dataframe(os.path.join(output_dir, 'predictions.tsv'), df_prediction)


if __name__ == '__main__':
    main(sys.argv[1:])
