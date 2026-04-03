from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin, UserProfileUpdate
from app.services.auth_service import (
    register_user,
    login_user,
    update_user_profile,
    calculate_account_completion
)
from app.services.user_service import (
    search_users_by_skill,
    match_users_by_skills
)
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.utils.response import success_response
from app.utils.skills import skills_to_list

router = APIRouter()


# DB Dependency
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
    updated_user = update_user_profile(
        db,
        current_user,
        payload.full_name,
        payload.phone,
        payload.skills
    )

    return success_response(
        data={
            "email": updated_user.email,
            "full_name": updated_user.full_name,
            "phone": updated_user.phone,
            "skills": skills_to_list(updated_user.skills),
            "account_completion": calculate_account_completion(updated_user)
        },
        message="Profile updated"
    )


@router.get("/me")
def get_profile(current_user: User = Depends(get_current_user)):
    return success_response(
        data={
            "email": current_user.email,
            "full_name": current_user.full_name,
            "phone": current_user.phone,
            "skills": skills_to_list(current_user.skills),
            "account_completion": calculate_account_completion(current_user)
        },
        message="User profile fetched"
    )


@router.get("/completion")
def get_completion(current_user: User = Depends(get_current_user)):
    return success_response(
        data={
            "account_completion": calculate_account_completion(current_user)
        },
        message="Account completion fetched"
    )


# =========================
# SEARCH
# =========================

@router.get("/users/search")
def search_users(
    skill: str = Query(...),
    level: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = search_users_by_skill(db, skill, level)

    results = []

    for user in users:
        results.append({
            "email": user.email,
            "full_name": user.full_name,
            "skills": skills_to_list(user.skills)
        })

    return success_response(
        data=results,
        message="Users fetched successfully"
    )


# =========================
# MATCHING (UPDATED)
# =========================

@router.get("/users/match")
def match_users(
    skills: str = Query(...),
    min_match: int = Query(1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill_list = skills.split(",")

    matches = match_users_by_skills(db, skill_list, min_match)

    results = []

    for m in matches:
        user = m["user"]

        results.append({
            "email": user.email,
            "full_name": user.full_name,
            "skills": skills_to_list(user.skills),
            "match_count": m["match_count"],
            "score": m["score"]
        })

    return success_response(
        data=results,
        message="Matched users successfully"
    )