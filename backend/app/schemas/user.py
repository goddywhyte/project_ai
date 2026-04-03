from pydantic import BaseModel, EmailStr, Field
from typing import List


class Skill(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    level: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfileUpdate(BaseModel):
    full_name: str = Field(None, min_length=2, max_length=100)
    phone: str = Field(None, min_length=7, max_length=20)
    skills: List[Skill] = []