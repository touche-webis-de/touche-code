FROM python:3

ADD predict.py requirements.txt /

RUN pip3 install -r /requirements.txt

ENTRYPOINT [ "/predict.py" ]
