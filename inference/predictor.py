import json
import logging
import re

import fasttext
import smart_open


class PythonPredictor:
    def __init__(self, config):
        self.config = config
        self.model = self.download_model()

    def download_model(self):
        if 's3://' in self.config['model_location']:
            model = smart_open.open(self.config['model_location'], 'rb').read()
            with open('model.bin', 'wb') as fh:
                fh.write(model)
            genre_model = fasttext.load_model('model.bin')
        else:
            genre_model = fasttext.load_model(self.config['model_location'])

        logging.info(f"Model loaded successfully from {self.config['model_location']}")
        return genre_model

    def aggressively_clean_text(self, t):
        """
        We don't have a properly defined shared library of code used in training + production yet
        :param t:
        :return:
        """
        t = t.lower()
        t = re.sub(r"\W", ' ', t)
        return t

    def predict(self, payload):
        cleaned_input = self.aggressively_clean_text(payload['data'])
        topn = 3
        if 'topn' in payload:
            topn = int(payload['topn'])
        pred_labels, confids = self.model.predict(cleaned_input, k=topn)
        label_prefix = "__label__"
        predictions = dict()
        for label, confidence in zip(pred_labels, confids):
            l = label.split(label_prefix)[1]
            predictions[l] = confidence
        return json.dumps({'prediction': predictions, 'labels': self.model.labels})
