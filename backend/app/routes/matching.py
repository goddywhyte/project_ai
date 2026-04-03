from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from app.services.matching_service import MatchingService
from app.services.user_service import UserService
from app.utils.response import success_response
from app.database.session import get_db

router = APIRouter(prefix="/match", tags=["Matching"])


@router.get("/")
def match_users(
    skills: List[str] = Query(...),
    min_match: int = Query(1, ge=1),
    min_level: str = Query("beginner"),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Match users using real database.
    """

    users = UserService.get_all_users_with_skills(db)

    results = MatchingService.match_users(
        users=users,
        required_skills=skills,
        min_match=min_match,
        min_level=min_level,
        role=role
    )

    return success_response(
        data=results,
        message="Users matched successfully"
    )