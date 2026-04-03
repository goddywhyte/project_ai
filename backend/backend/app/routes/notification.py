from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.notification_service import (
    get_user_notifications,
    mark_as_read
)
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.utils.response import success_response

router = APIRouter(prefix="/notifications")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifs = get_user_notifications(db, current_user.id)

    return success_response(data=[
        {
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifs
    ])


@router.post("/read/{notification_id}")
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = mark_as_read(db, notification_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")

    return success_response(message="Marked as read")