import pickle
import os

dirname = './checkpoints/human_value_trained_models'
filelist = os.listdir(dirname)

for file in filelist:
    if file.endswith('pkl'):
        with open(os.path.join(dirname, file), 'rb') as f:
            loaded_dict = pickle.load(f)
            print(loaded_dict)