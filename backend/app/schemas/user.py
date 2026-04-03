from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
import re


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SkillItem(BaseModel):
    name: str
    level: str

    @validator("level")
    def validate_level(cls, v):
        if v.lower() not in ["beginner", "intermediate", "expert"]:
            raise ValueError("Invalid level")
        return v.lower()


class UserProfileUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    skills: Optional[List[SkillItem]]

    @validator("full_name")
    def validate_name(cls, v):
        if v and re.search(r"\d", v):
            raise ValueError("Name cannot contain numbers")
        return v