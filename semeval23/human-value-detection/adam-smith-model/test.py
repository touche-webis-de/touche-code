import pickle
import os
import sys


def main(dirname):
    filelist = os.listdir(dirname)

    for file in filelist:
        if file.endswith('pkl'):
            with open(os.path.join(dirname, file), 'rb') as f:
                loaded_dict = pickle.load(f)
                print(loaded_dict)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        sys.exit(2)

    main(arguments[0])
