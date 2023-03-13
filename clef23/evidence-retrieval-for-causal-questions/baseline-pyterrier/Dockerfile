FROM webis/tira-ir-starter-chatnoir:0.0.2

RUN rm -f /workspace/*.ipynb

COPY sample-input/ /workspace/sample-input
COPY full-rank-pipeline.ipynb re-rank-pipeline.ipynb /workspace/

RUN jupyter trust /workspace/full-rank-pipeline.ipynb \
	&& jupyter trust /workspace/re-rank-pipeline.ipynb

