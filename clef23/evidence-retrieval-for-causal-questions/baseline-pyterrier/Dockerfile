FROM webis/tira-ir-starter-pyterrier:0.0.1-base

RUN pip3 install --no-deps chatnoir-pyterrier && pip3 install chatnoir_api

COPY sample-input/ /workspace/sample-input
COPY run-notebook.py full-rank-pipeline.ipynb re-rank-pipeline.ipynb tira_utils.py /workspace/

RUN jupyter trust /workspace/full-rank-pipeline.ipynb \
	&& jupyter trust /workspace/re-rank-pipeline.ipynb

