import pickle as pkl
import shutil
from abc import ABC, abstractmethod
from pathlib import Path

import cv2
import numpy as np
import onnxruntime
from numpy import dot
from numpy.linalg import norm


class Identification(ABC):
    def __init__(self):
        self.img_size = 112
        self.model_path = "models/model.onnx"
        self.model = self._load_model(self.model_path)
        self.path_out = "temp/out.png"
        self.path_all_embeddings = Path("data")

    def _load_model(self, model_path):
        self.session = onnxruntime.InferenceSession(
            str(model_path), providers=["CPUExecutionProvider"]
        )

    @abstractmethod
    def open_image(self):
        raise NotImplementedError

    def _preprocess_input(self, input):
        image = self.open_image(input)
        image = cv2.resize(image, (self.img_size, self.img_size))
        tensor = image[:, :, ::-1].transpose(2, 0, 1)
        tensor = np.ascontiguousarray(tensor, dtype=np.float32)
        tensor = tensor.astype(np.float32)
        tensor /= 255.0
        if len(tensor.shape) == 3:
            tensor = np.expand_dims(tensor, axis=0)
        return tensor

    def predict(self, input):
        resized_image = self._preprocess_input(input)
        pred = self.session.run(
            [self.session.get_outputs()[0].name],
            {self.session.get_inputs()[0].name: resized_image},
        )[0]
        return pred

    def cos(self, input):
        pred = self.predict(input)
        vectors = [x for x in self.path_all_embeddings.glob("**/*.pkl")]
        for path_vector in vectors:
            vector = np.array(pkl.load(open(str(path_vector), "rb"))[0])
            result = dot(vector, pred[0]) / (norm(vector) * norm(pred[0]))
            if result > 0.6:
                save_image_path = str(path_vector).replace(".pkl", ".jpg")
                pkl_path = str(path_vector).split("/")[-1]
                image_path = pkl_path.replace(".pkl", ".jpg")
                shutil.copy(save_image_path, f"temp/{image_path}")


class IdentificationBytes(Identification):
    def open_image(self, input):
        image = np.asarray(bytearray(input), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        return image


class IdentificationImages(Identification):
    def open_image(self, input):
        image = cv2.imread(input)
        return image
