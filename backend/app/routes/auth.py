from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import json

from app.database.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin, UserProfileUpdate
from app.services.auth_service import register_user, login_user
from app.services.file_service import save_file
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.utils.response import success_response
from app.utils.skills import skills_to_list

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# AUTH
# =========================

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(db, user.email, user.password)

    return success_response(
        data={"email": new_user.email},
        message="User created successfully"
    )


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token_data = login_user(db, user.email, user.password)

    return success_response(
        data=token_data,
        message="Login successful"
    )


# =========================
# PROFILE
# =========================

@router.put("/profile")
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.full_name = payload.full_name
    current_user.phone = payload.phone
    current_user.skills = json.dumps([s.dict() for s in payload.skills])

    db.commit()
    db.refresh(current_user)

    return success_response(message="Profile updated")


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return success_response(
        data={
            "email": current_user.email,
            "full_name": current_user.full_name,
            "phone": current_user.phone,
            "skills": skills_to_list(current_user.skills),
            "cv_file": current_user.cv_file,
            "profile_image": current_user.profile_image
        }
    )


# =========================
# FILE UPLOADS (SECURE)
# =========================

@router.post("/upload/cv")
def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    content = file.file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Max 5MB")

    file.file.seek(0)

    path = save_file(file, "cv")

    current_user.cv_file = path
    db.commit()

    return success_response(data={"cv_file": path})


@router.post("/upload/image")
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Invalid image")

    content = file.file.read()
    if len(content) > 3 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Max 3MB")

    file.file.seek(0)

    path = save_file(file, "images")

    current_user.profile_image = path
    db.commit()

    return success_response(data={"profile_image": path})