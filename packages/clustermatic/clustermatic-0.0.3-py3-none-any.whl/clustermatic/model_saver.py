import joblib
import os


class ModelSaver:
    def __init__(self, model, model_path):
        self.model = model
        self.model_path = model_path

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
