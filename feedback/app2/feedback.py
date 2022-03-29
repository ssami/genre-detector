from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import crud
from app_models import FeedbackModel
from feedback_db import FeedbackClient

app = FastAPI()
db_client = FeedbackClient()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/")
def pulse():
    return "hello world"


@app.get('/feedback', response_model=List[FeedbackModel])
def get_feedback(limit: int = 100):
    return crud.get_all_feedback(client=db_client, limit=limit)


@app.post("/feedback")
def create_feedback(data: FeedbackModel):
    return crud.create_feedback(client=db_client, info=data)
