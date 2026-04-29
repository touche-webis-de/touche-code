import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='A dummy evaluator that always outputs a score of 0')
    parser.add_argument("-p", "--predictions", help="path to the dir holding the predictions (in a folder for each dataset/task)", required=True)
    parser.add_argument("-t", "--truth", help="path to the dir holding the true labels (in a folder for each dataset/task)", required=True)
    parser.add_argument("-o", "--output", help="path to the dir to write the results to", required=True, type=Path)
    args = parser.parse_args()

    (args.output / "evaluation.prototext").write_text('measure{\n  key: "score"\n  value: "0"\n}\n')


if __name__ == "__main__":
    main()