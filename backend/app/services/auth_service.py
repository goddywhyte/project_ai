from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token


def register_user(db: Session, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Weak password")

    user = User(
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token}