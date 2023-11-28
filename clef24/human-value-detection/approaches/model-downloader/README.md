# Huggingface Model Downloader

For model files stored on the [Hugging Face Hub](https://huggingface.co/models) you can use the [download_model_files.py](download_model_files.py) to download them (works also in GitHub actions).

Adapt the [model_downloads.jsonl](model_downloads.jsonl) to the models you need. Then
```bash
python3 download_model_files.py -f model_downloads.jsonl
```
Use `-t <token>` to pass a Hugging Face Hub access token.

