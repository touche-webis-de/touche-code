from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd
import re
import statistics


baseline_results = Path("../results.jsonl")
image_embeddings = Path("../../../indexing/image_embeddings.csv")
argument_embeddings = Path("../../../indexing/argument_embeddings.csv")
core_aspects_embeddings = Path("../../../indexing/core_aspects_embeddings.csv")

images_embedding_df = pd.read_csv(image_embeddings)
argument_embedidng_df = pd.read_csv(argument_embeddings)
core_aspects_embedding_df = pd.read_csv(core_aspects_embeddings)

# get all image ids for a given argument id
def get_images_for_argument(argument_id):
    image_ids = []
    with open(baseline_results, "r") as file:
        for line in file:
            result = json.loads(line)
            if result["argument_id"] == argument_id:
                image_ids.append(result["image_id"])
    return image_ids


# get all distinct argument ids from the baseline results
def get_argument_ids():
    argument_ids = []
    with open(baseline_results, "r") as file:
        for line in file:
            result = json.loads(line)
            arg_id = result["argument_id"]
            if arg_id not in argument_ids:
                argument_ids.append(result["argument_id"])
    return argument_ids


# Get the image embeddings by the image_id from the image_embeddings.csv file
def get_image_embeddings_from_id(image_id):
    matching_row = images_embedding_df.loc[images_embedding_df['image_id'] == image_id]

    if not matching_row.empty:
        # Convert the string representation of the embedding to a list of floats
        embedding_str = matching_row['image_embedding'].values[0]  # Get the string value
        embedding_list = embedding_str.split(" ")

        flat_list = [re.sub(r'[\[\]\n]', '', item) for sublist in embedding_list for item in sublist.split()]
        flat_list = [item for item in flat_list if item]
        float_values = [float(x) for x in flat_list]
        return float_values

    else:
        # Handle the case where no matching row is found
        return None
    
# returns the embeddings aóf an argument by its argument_id
def argument_embedding_from_id(argument_id):
    matching_row = argument_embedidng_df.loc[argument_embedidng_df['argument_id'] == argument_id]

    if not matching_row.empty:
        # Convert the string representation of the embedding to a list of floats
        embedding_str = matching_row['argument_embedding'].values[0]  # Get the string value
        embedding_list = embedding_str.split(" ")

        flat_list = [re.sub(r'[\[\]\n]', '', item) for sublist in embedding_list for item in sublist.split()]
        flat_list = [item for item in flat_list if item]
        float_values = [float(x) for x in flat_list]
        return float_values

    else:
        # Handle the case where no matching row is found
        return None
    

# get embeddings of the core aspects of an argument by its argument_id
def core_aspects_embedding_from_id(argument_id):
    matching_row = core_aspects_embedding_df.loc[core_aspects_embedding_df['argument_id'] == argument_id]

    if not matching_row.empty:
        # Convert the string representation of the embedding to a list of floats
        embedding_str = matching_row['core_aspects_embedding'].values[0]  # Get the string value
        embedding_list = embedding_str.split(" ")

        flat_list = [re.sub(r'[\[\]\n]', '', item) for sublist in embedding_list for item in sublist.split()]
        flat_list = [item for item in flat_list if item]
        float_values = [float(x) for x in flat_list]
        return float_values

    else:
        # Handle the case where no matching row is found
        return None
    

# Calculate the cosine similarity between one argument and its image embeddings and return the mean value    
def get_cosine_similarity_for_argument(argument_id, by_core_aspects=True):
    if by_core_aspects:
        argument_embedding = core_aspects_embedding_from_id(argument_id)
    else:
        argument_embedding = argument_embedding_from_id(argument_id)

    if argument_embedding is None:
        return None

    image_ids = get_images_for_argument(argument_id)
    image_embeddings = [get_image_embeddings_from_id(image_id) for image_id in image_ids]

    similarities = []
    for image_embedding in image_embeddings:
        if image_embedding is None:
            continue
        similarity = cosine_similarity([argument_embedding], [image_embedding])
        similarities.append(similarity[0][0])

    erg = [float(x) for x in similarities]
    mean = statistics.mean(erg)
    return erg, mean


# return the cosine similarity matrix between all images of an argument
def get_cosine_similarities_between_images(argument_id):
    argument_embedding = argument_embedding_from_id(argument_id)
    if argument_embedding is None:
        return None

    image_ids = get_images_for_argument(argument_id)
    image_embeddings = [get_image_embeddings_from_id(image_id) for image_id in image_ids]

    similarity_matrix = cosine_similarity(image_embeddings)
    return similarity_matrix

# generates and prints the results of the cosine similarity for the arguments
def print_similarity_of_each_argument_results():
    argument_ids = get_argument_ids()
    similarities = []
    for argument_id in argument_ids:
        erg, mean = get_cosine_similarity_for_argument(argument_id)
        if mean is not None:
            similarities.append(mean)

    # for each argument, calculate the cosine similiarity between the argument and all of its images individually
    # then calculate the mean of all the cosine similarities to get one value for each of the 13 arguments

    print(f"Similarity Scores: {similarities}")
    print(f"Number of arguments: {len(similarities)}")
    print(f"Mean cosine similarity of all arguments: {statistics.mean(similarities)}")
    print(f"Standard deviation of cosine similarities: {statistics.stdev(similarities)}")
    print(f"Min cosine similarity: {min(similarities)}")
    print(f"Max cosine similarity: {max(similarities)}")


def calculate_metrics_images(argument_id):
    similarity_matrix = get_cosine_similarities_between_images(argument_id)
    if similarity_matrix is None:
        return None
    erg = []
    for row in similarity_matrix:
        for num in row:
            if round(num, 2) != 1.0:
                erg.append(num)
    erg = set(erg)
    print(f"Argument ID: {argument_id}")
    print(f"Mean similarity: {statistics.mean(erg)}")
    print(f"Max similarity: {max(erg)}")
    print(f"Min similarity: {min(erg)}")

if __name__ == "__main__":
    
    print_similarity_of_each_argument_results()
    
    # arg_ids = get_argument_ids()
    # for arg_id in arg_ids:
    #     calculate_metrics_images(arg_id)
    

