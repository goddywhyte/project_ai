from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.utils.phone import normalize_phone
from app.utils.skills import normalize_skills


def register_user(db: Session, email: str, password: str):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email exists")

    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(400, "Invalid credentials")

    return {"access_token": create_access_token({"sub": user.email})}


def update_user_profile(db, user, full_name=None, phone=None, skills=None):
    if full_name:
        user.full_name = full_name

    if phone:
        phone = normalize_phone(phone)

        existing = db.query(User).filter(User.phone == phone).first()
        if existing and existing.id != user.id:
            raise HTTPException(400, "Phone already used")

        user.phone = phone

    if skills:
        user.skills = normalize_skills([s.dict() for s in skills])

    db.commit()
    db.refresh(user)
    return user


def calculate_account_completion(user):
    score = 0
    if user.email: score += 25
    if user.full_name: score += 25
    if user.phone: score += 25
    if user.skills: score += 25
    return score