from transformers import (AutoTokenizer, AutoConfig, AutoModel)
import os


transformer_dir = '/app/transformers'


def __set_transformer_dir__(p_transformer_dir: str):
    global transformer_dir
    transformer_dir = p_transformer_dir


def download_model_data(source_path: str):
    print(f'Downloading model data for: {source_path}')
    local_path = os.path.join(transformer_dir, source_path)
    if not os.path.exists(local_path) or not os.path.isdir(local_path):
        os.makedirs(local_path)

    tokenizer = AutoTokenizer.from_pretrained(source_path)
    config = AutoConfig.from_pretrained(source_path)
    model = AutoModel.from_pretrained(source_path, return_dict=True)

    tokenizer.save_pretrained(local_path)
    config.save_pretrained(local_path)
    model.save_pretrained(local_path)


def load_local_tokenizer(source_path: str):
    local_path = os.path.join(transformer_dir, source_path)
    if not os.path.exists(local_path):
        raise RuntimeError(f'No local directory for {source_path}')
    tokenizer = AutoTokenizer.from_pretrained(local_path)
    return tokenizer


def load_local_model(source_path: str, **args):
    local_path = os.path.join(transformer_dir, source_path)
    if not os.path.exists(local_path):
        raise RuntimeError(f'No local directory for {source_path}')
    model = AutoModel.from_pretrained(local_path, **args)
    return model
