from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from feedback.obj_models import FeedbackModel, FeedbackOrm, Base
from feedback.feedback_db import SessionLocal, engine
from feedback import crud

app = FastAPI()
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def pulse():
    return "hello world"


@app.get('/feedback/{model_id}', response_model=List[FeedbackOrm])
def get_feedback(model_id, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_feedback_for_model(db=db, skip=skip, limit=limit, model_id=model_id)


@app.post("/feedback", response_model=FeedbackOrm)
def create_feedback(data: FeedbackModel, db: Session = Depends(get_db)):
    return crud.create_feedback(db=db, feedback=data)
