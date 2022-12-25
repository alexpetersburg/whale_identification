import pickle as pkl
from pathlib import Path

from tqdm import tqdm

from tools import IdentificationImages

path = Path("data")

if __name__ == "__main__":
    img_path_list = [x for x in path.glob(f"**/*.jpg")]
    for img in tqdm(img_path_list):
        id = IdentificationImages()
        embeddings = id.predict(str(img))
        embedding_path = str(img).replace(".jpg", ".pkl")
        pkl.dump(embeddings, open(f"{embedding_path}", "wb"))
