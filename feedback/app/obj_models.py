from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from app.feedback_db import Base


class Feedback(Base):
    """
    A SQLAlchemy ORM model
    """
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, index=True)
    text = Column(String, unique=True)
    label = Column(String)


class FeedbackModel(BaseModel):
    """
    A Pydantic model
    """
    model_id: int
    text: str
    label: str


class FeedbackOrm(FeedbackModel):
    """
    A Pydantic model with ORM extension
    """
    id: int

    class Config:
        orm_mode = True
