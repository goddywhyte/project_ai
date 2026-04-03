from sqlalchemy.orm import Session
from sqlalchemy import desc
import json

from app.models.job import Job
from app.models.user import User
from app.models.application import Application
from app.models.saved_job import SavedJob
from app.services.notification_service import create_notification

LEVEL_SCORE = {
    "beginner": 1,
    "intermediate": 2,
    "expert": 3
}


def get_all_jobs(db: Session, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit

    return db.query(Job)\
        .order_by(desc(Job.created_at))\
        .offset(offset)\
        .limit(limit)\
        .all()


def apply_to_job(db: Session, user_id: int, job_id: int):
    existing = db.query(Application).filter(
        Application.user_id == user_id,
        Application.job_id == job_id
    ).first()

    if existing:
        return None

    app = Application(user_id=user_id, job_id=job_id)
    db.add(app)
    db.commit()

    create_notification(db, user_id, f"Applied to job {job_id}")

    return app


def get_saved_jobs(db: Session, user_id: int):
    records = db.query(SavedJob).filter(
        SavedJob.user_id == user_id
    ).all()

    job_ids = [r.job_id for r in records]

    jobs = db.query(Job).filter(Job.id.in_(job_ids)).all()

    return [{"id": j.id, "title": j.title} for j in jobs]


def match_users_to_job(db: Session, job_id: int):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None

    required_skills = job.required_skills.split(",")
    users = db.query(User).filter(User.skills.isnot(None)).all()

    results = []

    for user in users:
        user_skills = json.loads(user.skills)

        match_count = sum(
            1 for req in required_skills
            for s in user_skills if s["name"] == req
        )

        if match_count:
            score = match_count * 10
            results.append({
                "user": user,
                "match_percentage": int((match_count / len(required_skills)) * 100),
                "score": score
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)


def get_ranked_applicants(db: Session, job_id: int):
    apps = db.query(Application).filter(
        Application.job_id == job_id
    ).all()

    user_ids = [a.user_id for a in apps]

    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return [{"email": u.email} for u in users]