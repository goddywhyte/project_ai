from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.job import Job
from app.models.application import Application


def get_analytics_overview(db: Session):
    return {
        "users": db.query(func.count(User.id)).scalar(),
        "jobs": db.query(func.count(Job.id)).scalar(),
        "applications": db.query(func.count(Application.id)).scalar()
    }