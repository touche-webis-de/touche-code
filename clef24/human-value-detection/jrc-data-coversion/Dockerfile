FROM python:3.10

COPY requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

COPY convert_annotations.py /convert_annotations.py
ENTRYPOINT [ "python3", "/convert_annotations.py", "--input" ]
