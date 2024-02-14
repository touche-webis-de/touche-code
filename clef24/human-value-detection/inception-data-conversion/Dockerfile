FROM python:3.10

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY convert_curation.py /convert_curation.py
ENTRYPOINT [ "python3", "/convert_curation.py", "--input" ]

