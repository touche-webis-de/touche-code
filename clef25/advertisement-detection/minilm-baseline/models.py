import torch as T
import torch.nn.functional as F
from transformers import AutoModel


MODEL_DICT = {"all-MiniLM-L6-v2": 384, "all-mpnet-base-v2": 768}


class SupervisedModel(T.nn.Module):
    def __init__(self, sbert_model: str):
        super(SupervisedModel, self).__init__()

        # Encoder
        self.encoder = AutoModel.from_pretrained(f"sentence-transformers/{sbert_model}")

        # Output layer
        hidden_size = MODEL_DICT[sbert_model]
        self.linear = T.nn.Linear(hidden_size, 1)



    def feed(self, x):
        """
        Calculates the embeddings based on tokens, attention_masks and token_type_ids
        :param x:   Input dictionary
        :return:    Normalized embedding
        """

        # Encode the input
        output = self.encoder(**x)
        embedding = mean_pooling(output, x['attention_mask'])

        # Return the normalized embedding
        return F.normalize(embedding, p=2, dim=1)


    def forward(self, batch: dict):
        """
        Function that takes in a dictionary for the current batch that contains tokenized sentence pairs of the form

        {"input_ids": tensor([[...]]), "attention_mask": tensor([[...]]), "token_type_ids": tensor([[..]])}

        and returns a prediction for whether they are paraphrases

        :param batch            The batch of tokenized sentence pairs produced by a dataloader.
        :return:                The predictions for the sentence pairs
        """

        # Drop the labels
        batch.pop("labels", None)

        # Calculate the embeddings for the sentence pairs in the batch
        embeddings = self.feed(batch)

        # Return the results of the sigmoid
        logits = self.linear(embeddings)
        return logits

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return T.sum(token_embeddings * input_mask_expanded, 1) / T.clamp(input_mask_expanded.sum(1), min=1e-9)
