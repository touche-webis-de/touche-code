FROM webis/tira-ir-starter-pyterrier:0.0.1-base

RUN pip3 install chatnoir-pyterrier

COPY sample-input full-rank-pipeline.ipynb re-rank-pipeline.ipynb /workspace/

RUN jupyter trust /workspace/full-rank-pipeline.ipynb \
	&& jupyter trust /workspace/re-rank-pipeline.ipynb

