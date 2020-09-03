import re

import fasttext as ft
import json

from inference.exceptions import ConfigException
import boto3
import os
import logging


class PythonPredictor:
    def __init__(self, config):
        self.config = config
        self.model = self.download_model()

    def download_model(self):
        req_configs = ['model_bucket', 'model_key']
        for config_key in req_configs:
            if config_key not in self.config:
                raise ConfigException(f'No {config_key} defined')

        s3_client = boto3.client('s3')
        local_file_name = os.path.split(self.config['model_key'])[-1]
        local_file_path = os.path.join('/tmp', local_file_name)
        logging.info(f"Model downloaded from {self.config['model_bucket']}/{self.config['model_key']} "
                     f"and stored in {local_file_path}")
        buckets = s3_client.list_buckets()
        logging.info(buckets)
        with open(local_file_path, 'wb') as wh:
            s3_client.download_fileobj(self.config['model_bucket'], self.config['model_key'], wh)
        genre_model = ft.load_model(local_file_path)
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
        pred_labels, confids = self.model.predict(cleaned_input, k=3)
        label_prefix = "__label__"
        predictions = dict()
        for label, confidence in zip(pred_labels, confids):
            l = label.split(label_prefix)[1]
            predictions[l] = confidence
        return json.dumps({'prediction': predictions})
