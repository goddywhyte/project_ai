from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.admin_service import get_analytics_overview
from app.auth.admin import get_admin_user
from app.utils.response import success_response

router = APIRouter(prefix="/admin")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics")
def analytics(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return success_response(data=get_analytics_overview(db))