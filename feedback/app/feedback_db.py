import os
from typing import List

from app.db_models import FeedbackModel
from pymongo import MongoClient


class FeedbackClient():
    DB = "feedback"
    COLLECTION = "fdbk"

    def __init__(self):
        self.client = MongoClient(FeedbackClient.__uri_construction())

    @classmethod
    def __uri_construction(cls):
        # if not os.environ['MONGO_USER'] or not os.environ['MONGO_PASSWORD']:
        #     raise RuntimeError('Mongo credentials needed!')
        # username = urllib.parse.quote_plus(os.environ['MONGO_USER'])
        # password = urllib.parse.quote_plus(os.environ['MONGO_PASSWORD'])
        host = os.environ['MONGO_HOST']
        port = os.environ['MONGO_PORT']

        # return f"mongodb://{username}:{password}@{host}:{port}"
        return f"mongodb://{host}:{port}"

    def insert_feedback(self, feedback: FeedbackModel):
        resp = self.client[self.DB][self.COLLECTION].insert_one(feedback.dict())
        return resp.inserted_id

    def get_feedback(self, limit=10) -> List[FeedbackModel]:
        collection = self.client[self.DB][self.COLLECTION]
        results = []
        for feedback in collection.find(limit=limit):
            results.append(FeedbackModel(**feedback))   # unpack DB fields into Pydantic model
        return results
