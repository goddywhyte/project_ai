from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.job_service import get_all_jobs
from app.utils.response import success_response
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/jobs")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_jobs(
    page: int = Query(1),
    limit: int = Query(10),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    jobs = get_all_jobs(db, page, limit)

    return success_response(
        data=[{"id": j.id, "title": j.title} for j in jobs]
    )