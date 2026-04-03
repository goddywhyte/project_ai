from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime

from app.database.base import Base


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    created_at = Column(DateTime, default=datetime.utcnow)