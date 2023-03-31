from transformers import (AutoTokenizer, AutoConfig)


def main():
    tokenizer_dir = "/workspace/tokenizer"

    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    config = AutoConfig.from_pretrained('bert-base-uncased')

    tokenizer.save_pretrained(tokenizer_dir)
    config.save_pretrained(tokenizer_dir)


if __name__ == '__main__':
    main()
