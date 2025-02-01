# there are copies of the image dataset in the directories only_text_images and no_text_images
# and the irrelevant images get removed from either dataset

import shutil
from pathlib import Path
import os

images_with_text_ds_dir = Path('./only_text_images')
images_without_text_ds_dir = Path('./no_text_images')

def prepare_text_dataset(base_path):
    # removes images without text from the dataset
    cnt = 0
    for prefix_dir in os.listdir(base_path):
        prefix_path = os.path.join(base_path, prefix_dir)
        if os.path.isdir(prefix_path): 
            for image_hash_dir in os.listdir(prefix_path):
                image_dir = os.path.join(prefix_path, image_hash_dir)
                if os.path.isdir(image_dir): 
                    image_text = load_file(os.path.join(image_dir, "image-text.txt"))
                    if image_text is None or len(image_text) <= 2:
                        shutil.rmtree(image_dir)
                        cnt += 1
    return cnt

def prepare_no_text_dataset(base_path):
    # removes images with text from the dataset
    cnt = 0
    for prefix_dir in os.listdir(base_path):
        prefix_path = os.path.join(base_path, prefix_dir)
        if os.path.isdir(prefix_path): 
            for image_hash_dir in os.listdir(prefix_path):
                image_dir = os.path.join(prefix_path, image_hash_dir)
                if os.path.isdir(image_dir): 
                    image_text = load_file(os.path.join(image_dir, "image-text.txt"))
                    if len(image_text) > 2:
                        shutil.rmtree(image_dir)
                        cnt += 1
    return cnt

def load_file(filepath):
    """help-function: reading text-files"""
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None


if __name__ == '__main__':

    removed_no_text_images = prepare_text_dataset(images_with_text_ds_dir)
    removed_text_images = prepare_no_text_dataset(images_without_text_ds_dir)

    print(f"Removed {removed_no_text_images} no-text images from the dataset")
    print(f"Removed {removed_text_images} text images from the dataset")

    # Removed 261 no-text images from the dataset
    # Removed 734 text images from the dataset