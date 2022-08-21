from typing import List

from app.db_models import FeedbackModel
from app.feedback_db import FeedbackClient


def create_feedback(client: FeedbackClient, info: FeedbackModel):
    return client.insert_feedback(info)


def get_all_feedback(client: FeedbackClient, limit=10) -> List[FeedbackModel]:
    return client.get_feedback(limit)
