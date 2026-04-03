from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)
    password = Column(String)

    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    skills = Column(String, nullable=True)

    cv_file = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)