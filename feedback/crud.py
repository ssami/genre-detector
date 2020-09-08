from sqlalchemy.orm import Session

from feedback import obj_models


def get_feedback_for_model(db: Session, model_id: int, skip: int = 0, limit: int = 100):
    return db.query(obj_models.Feedback)\
        .filter(obj_models.Feedback.model_id == model_id)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_feedback(db: Session, feedback: obj_models.FeedbackModel):
    db_item = obj_models.Feedback(**feedback.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

