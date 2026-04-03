from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)
    description = Column(String)

    required_skills = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)