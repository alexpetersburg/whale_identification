import pandas as pd
import os
import shutil

if __name__ == '__main__':
    out_dataset_dir = os.path.join('data', 'whale_recognition_without_new')

    annotation = pd.read_csv(os.path.join('whale_dataset', 'train.csv'))
    new_whale_counter = 0
    for _, row in annotation.iterrows():
        whale_id, image_name = row["Id"], row["Image"]
        if whale_id == "new_whale":
            whale_dir = os.path.join(out_dataset_dir, f'{whale_id}_{new_whale_counter}')
            new_whale_counter += 1
        else:
            whale_dir = os.path.join(out_dataset_dir, whale_id)
        os.makedirs(whale_dir, exist_ok=True)
        shutil.copyfile(os.path.join('whale_dataset', 'train', image_name), os.path.join(whale_dir, image_name))
