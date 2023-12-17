# Uncomment lines for GUI BUILD
FROM webis/vuetify-dev-container:0.1

COPY vuetify-resources/result-rendering-with-vue/ /workspace/

RUN cd /workspace/
RUN yarn build

FROM python:3.10

RUN pip install "numpy>=1.25.2" "pandas>=2.0.3" "scikit-learn>=1.3.1"
COPY evaluator.py /evaluator.py

COPY --from=0 /workspace/dist/ /

ENTRYPOINT [ "python3", "evaluator.py" ]
