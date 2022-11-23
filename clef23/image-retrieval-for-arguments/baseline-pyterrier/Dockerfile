FROM webis/tira-ir-starter-pyterrier:0.0.1-base

COPY sample-input /workspace/sample-input
COPY full-rank-pipeline.ipynb re-rank-pipeline.ipynb run-notebook.py tira_utils.py /workspace/

RUN jupyter trust /workspace/full-rank-pipeline.ipynb \
	&& jupyter trust /workspace/re-rank-pipeline.ipynb

