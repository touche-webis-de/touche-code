import sys
import os

############################################
#   Download files from Google Drive   #####
# https://stackoverflow.com/a/39225272 #####
############################################

import requests


def download_file_from_google_drive(id: str, destination: str):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = __get_confirm_token__(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    __save_response_content__(response, destination)


def __get_confirm_token__(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def __save_response_content__(response, destination: str):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


############################################


def main(destination_folder):
    files = {
        'HCV-409-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '11bt8WAeyEG14akTdqedTrd8Pmq1AwENX',
        'HCV-409_PARAMS.pkl': '11iW8tiLU80dLFtHBnrWh-tM2IV23q16x',
        'HCV-408-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '1116wn9BSXJtyoqX0_LPKhafgISTfRXrH',
        'HCV-408_PARAMS.pkl': '113c5xV3Gug2pXz-Lj7DWcNfDlzmmc42h',
        'HCV-406-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '10d5Axr8Jx3T8BG24BfgpYMN4CaNX2NVQ',
        'HCV-406_PARAMS.pkl': '10fSxwDftudkTzvf95NQwmGX9eLD8-WAV',
        'HCV-402-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '1-SlzK91dFOufFf7fXWmclRpcPgu6cc4m',
        'HCV-402_PARAMS.pkl': '1-VyCuP4ExPq5xN3PgkEgiLvAXmlVKp-i',
        'HCV-403-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '1-uM35yfpTQG_v1Hm8BMzH-qv5LoJXV_U',
        'HCV-403_PARAMS.pkl': '1-wEpkmZ3XqfcNvphrl9DjCdOCU9oMAEh',
        'HCV-405-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '10IyLQEc3P9nqAKFDZtT188jhbuZO95rv',
        'HCV-405_PARAMS.pkl': '10PXCYOpYM2HFFNLhM4iEBEcDq8Qne7rx',
        'HCV-364-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '13ZgoXwPYs-_PksacIe-fVF9oPnkLKrHl',
        'HCV-364_PARAMS.pkl': '13mxA4Zlh1YuK0AKcx8DfZzAmrOSLWKqc',
        'HCV-366-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '13r8i42P5pueBn1KKB-w2h4Xfzu4q33Bz',
        'HCV-366_PARAMS.pkl': '14-1urPo-gl3Nt9xF5Sk7yHIzEZI0ANlR',
        'HCV-368-microsoft-deberta-large-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '14jZF5an835ePTAMFHeMWyNKkQVgCEGWX',
        'HCV-368_PARAMS.pkl': '14q0Y80QOZu0kV6arZK9SSHGVYJIsdnVY',
        'HCV-371-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '15Mk3ap7hY0m9MkjWewVETo8qhuNhjOle',
        'HCV-371_PARAMS.pkl': '15kEopQtBqorNvF1taNWrgKhxHwGxVNy0',
        'HCV-372-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '15yWZdKmqc0mPKdq3NQ59vUfRNi0nJp1N',
        'HCV-372_PARAMS.pkl': '167ML7j9li5W_3-IMw9xsoW3Gf0sIURlV',
        'HCV-375-danschr-roberta-large-BS_16-EPOCHS_8-LR_5e-05-ACC_GRAD_2-MAX_LENGTH_165-BS_8-LR_2e-05-HL_None-DROPOUT_None-SL_None.ckpt': '16gqFOK5JILnE-gMs2sYgk3wiPuxEFHUd',
        'HCV-375_PARAMS.pkl': '16l_SxCpYhyphJNIha_sdb_sjJpuZIl9o'
    }
    for filename in files.keys():
        file_id = files[filename]
        destination = os.path.join(destination_folder, filename)
        download_file_from_google_drive(file_id, destination)


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if len(arguments) != 1:
        sys.exit(2)

    if not os.path.isdir(arguments[0]):
        sys.exit(2)

    main(arguments[0])
