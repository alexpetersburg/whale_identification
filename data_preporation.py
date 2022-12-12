import os
import shutil
from pathlib import Path
from typing import List

import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm


class Data:
    def __init__(self) -> None:
        self.annotation = pd.read_csv(os.path.join("whale_dataset", "train.csv"))
        self.out_dataset_dir = os.path.join("data", "whale_recognition_without_new")
        self.new_whale_counter = 0
        self.trashold_new_whale_counter = 110

    def _update_validation(self):
        # Validation set: sampled 400 identities that has 2 images + 110 new whales
        # Training set: all images except new whales

        path_class = [x for x in Path(self.out_dataset_dir).iterdir() if x.is_dir()]
        for class_whale in tqdm(path_class, desc="create val/train set"):
            name = str(class_whale).split("/")[-1]
            image = [x for x in class_whale.glob("**/*.jpg")]
            if len(image) >= 2:            
                os.makedirs(f"data/new_data/{name}", exist_ok=True)
                [shutil.copyfile(x, f"data/new_data/{name}/{str(x).split('/')[-1]}") for x in image]
            else:
                os.makedirs(f"data/train_data/{name}", exist_ok=True)
                [shutil.copyfile(x, f"data/train_data/{name}/{str(x).split('/')[-1]}") for x in image]
            
    def _split_dataset(self):
        whales = os.listdir('data/new_data')
        train_whales, test_whales = train_test_split(whales, test_size=0.1)
        for whale_id in train_whales:
            shutil.copytree(
                os.path.join(self.out_dataset_dir , whale_id), os.path.join("data", "train_data", whale_id)
            )
        for whale_id in test_whales:
            shutil.copytree(
                os.path.join(self.out_dataset_dir , whale_id), os.path.join("data", "test_data", whale_id)
            )
            
    def _create_dataset(self):
        for _, row in self.annotation.iterrows():
            whale_id, image_name = row["Id"], row["Image"]
            if whale_id == "new_whale":
                if self.new_whale_counter < self.trashold_new_whale_counter:
                    whale_dir = os.path.join(self.out_dataset_dir, f"{whale_id}")
                self.new_whale_counter += 1
            else:
                whale_dir = os.path.join(self.out_dataset_dir, whale_id)
            os.makedirs(whale_dir, exist_ok=True)
            shutil.copyfile(
                os.path.join("whale_dataset", "train", image_name),
                os.path.join(whale_dir, image_name),
            )


if __name__ == "__main__":
    data_created = Data()
    data_created._create_dataset()
    data_created._update_validation()
    data_created._split_dataset()
