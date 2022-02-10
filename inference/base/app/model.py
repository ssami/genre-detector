import os
import fasttext


MODEL_PATH_ENV = 'MODEL_PATH'


class LoadedModel:

    model = None

    def __init__(self):
        model_path = os.getenv(MODEL_PATH_ENV)
        if model_path:
            self.model = fasttext.load_model(model_path)
        else:
            raise RuntimeError("Model not found at " + MODEL_PATH_ENV)

    def predict(self, text, k=1):
        return self.model.predict(text, k)
