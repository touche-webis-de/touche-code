import os
import pandas as pd
import numpy as np
import torch
import clip
from PIL import Image
import xml.etree.ElementTree as ET

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
images_dir = './images'
args_dir = './arguments.xml'
csv_image_results = './image_embeddings.csv'
csv_args_results = './argument_embeddings.csv'

embedding_df = pd.DataFrame(columns=['image_id', 'image_embedding'])
argument_embedding_df = pd.DataFrame(columns=['argument_id', 'argument_embedding'])


def encode_images(images_dir):
    cnt = 0
    for prefix_dir in os.listdir(images_dir):
        prefix_path = os.path.join(images_dir, prefix_dir)
        if os.path.isdir(prefix_path): 
            for image_hash_dir in os.listdir(prefix_path):
                image_dir = os.path.join(prefix_path, image_hash_dir)
                if os.path.isdir(image_dir): 
                    
                    image_file = os.path.join(image_dir, "image.webp")
                    image_vector = []

                    # process the .webp-image
                    if image_file.endswith(".webp"):
                        try:
                            # Load and preprocess the image
                            image = preprocess(Image.open(image_file)).unsqueeze(0).to(device)
                            
                            # Generate the embedding and save to dataframe
                            with torch.no_grad():
                                cnt += 1
                                print(f"Processing image {cnt}")
                                image_features = model.encode_image(image)
                                image_vector = image_features.cpu().numpy()
                                id = os.path.basename(image_dir)

                                embedding_df.loc[len(embedding_df)] = [id, image_vector]

                        except Exception as e:
                            print(f"Error processing {image_file}: {e}")

    # save all embeddings with id in csv                        
    embedding_df.to_csv(csv_image_results, index=False)


def encode_arguments(args_dir):

    tree = ET.parse(args_dir)
    root = tree.getroot()

    for arg in root.findall('.//argument'):
        # extract id and claim from arguments.xml
        arg_id = arg.find('id').text if arg.find('id') is not None else None
        claim = arg.find('claim').text if arg.find('claim') is not None else None
        
        # Process the claim
        if claim:
            try:
                # Tokenize and preprocess the claim
                text = clip.tokenize([claim]).to(device)
                
                # Generate the embedding and save to dataframe
                with torch.no_grad():
                    print(f"Processing argument {arg_id}")
                    text_features = model.encode_text(text)
                    text_vector = text_features.cpu().numpy()

                    argument_embedding_df.loc[len(argument_embedding_df)] = [arg_id, text_vector]

            except Exception as e:
                print(f"Error processing argument {arg_id}: {e}")

    # Save all argument embeddings with id in csv
    argument_embedding_df.to_csv(csv_args_results, index=False)


if __name__ == "__main__":
    print("\n### Encoding images and arguments ###")
    encode_images(images_dir)
    #encode_arguments(args_dir)