import sys
import zipfile


def main(zip_file_path: str, destination_folder: str):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    main(arguments[0], arguments[1])
