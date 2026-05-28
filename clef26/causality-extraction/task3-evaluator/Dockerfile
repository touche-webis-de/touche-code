FROM python:3.11-slim

ENV HF_HUB_OFFLINE=1
ENV HF_HOME=/opt/hf-cache

RUN <<EOF
pip install pandas evaluate scikit-learn
python3 -c "import evaluate; evaluate.load('f1'); evaluate.load('precision'); evaluate.load('recall')"
EOF

ADD evaluator.py /