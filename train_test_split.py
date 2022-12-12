import os
import shutil
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    dataset_dir = os.path.join('data', 'whale_recognition_without_new')
    out_dataset_dir = os.path.join('data', 'whale_recognition_without_new_splitted')
    os.makedirs(out_dataset_dir, exist_ok=True)

    whales = os.listdir(dataset_dir)
    train_whales, test_whales = train_test_split(whales, test_size=0.1)
    for whale_id in train_whales:
        shutil.copytree(os.path.join(dataset_dir, whale_id), os.path.join(out_dataset_dir, 'train', whale_id))
    for whale_id in test_whales:
        shutil.copytree(os.path.join(dataset_dir, whale_id), os.path.join(out_dataset_dir, 'test', whale_id))
