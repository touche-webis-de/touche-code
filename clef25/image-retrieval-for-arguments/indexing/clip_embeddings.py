import os
import pandas as pd
import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
images_dir = './images'
csv_results = './image_embeddings.csv'

embedding_df = pd.DataFrame(columns=['image_id', 'image_embedding'])


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
    embedding_df.to_csv(csv_results, index=False)

encode_images(images_dir)