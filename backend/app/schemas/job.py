from pydantic import BaseModel
from typing import List


class JobCreate(BaseModel):
    title: str
    description: str = None
    required_skills: List[str]