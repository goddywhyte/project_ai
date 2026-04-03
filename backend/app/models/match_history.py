from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base


class MatchHistory(Base):
    __tablename__ = "match_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    searched_skills = Column(String, nullable=False)

    match_count = Column(Integer)
    match_percentage = Column(Integer)
    score = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)