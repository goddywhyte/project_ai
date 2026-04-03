import json
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.match_history import MatchHistory

LEVEL_SCORE = {
    "beginner": 1,
    "intermediate": 2,
    "expert": 3
}


def search_users_by_skill(db: Session, skill: str, level: str = None):
    skill = skill.lower()
    level = level.lower() if level else None

    users = db.query(User).all()
    results = []

    for user in users:
        if not user.skills:
            continue

        skills = json.loads(user.skills)

        for s in skills:
            if s["name"] == skill:
                if level and s["level"] != level:
                    continue

                score = LEVEL_SCORE.get(s["level"], 0)

                results.append({
                    "user": user,
                    "score": score
                })
                break

    results.sort(key=lambda x: x["score"], reverse=True)

    return [r["user"] for r in results]


def match_users_by_skills(
    db: Session,
    required_skills: list,
    weights: list = None,
    min_match: int = 1,
    must_have: list = None
):
    required_skills = [s.strip().lower() for s in required_skills]
    total_required = len(required_skills)

    if not weights or len(weights) != total_required:
        weights = [1] * total_required
    else:
        weights = [int(w) for w in weights]

    must_have = [s.strip().lower() for s in must_have] if must_have else []

    users = db.query(User).all()
    results = []

    for user in users:
        if not user.skills:
            continue

        user_skills = json.loads(user.skills)
        user_skill_names = [s["name"] for s in user_skills]

        if must_have:
            if not all(skill in user_skill_names for skill in must_have):
                continue

        match_count = 0
        weighted_score = 0

        for i, req in enumerate(required_skills):
            for s in user_skills:
                if s["name"] == req:
                    match_count += 1
                    level_score = LEVEL_SCORE.get(s["level"], 0)
                    weighted_score += level_score * weights[i]
                    break

        if match_count >= min_match:
            final_score = (match_count * 10) + weighted_score
            match_percentage = int((match_count / total_required) * 100)

            missing_skills = [
                skill for skill in required_skills
                if skill not in user_skill_names
            ]

            recommended_skills = missing_skills.copy()

            results.append({
                "user": user,
                "score": final_score,
                "match_count": match_count,
                "match_percentage": match_percentage,
                "weighted_score": weighted_score,
                "missing_skills": missing_skills,
                "recommended_skills": recommended_skills
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


def save_match_history(
    db: Session,
    user_id: int,
    searched_skills: list,
    match_count: int,
    match_percentage: int,
    score: int
):
    record = MatchHistory(
        user_id=user_id,
        searched_skills=",".join(searched_skills),
        match_count=match_count,
        match_percentage=match_percentage,
        score=score
    )

    db.add(record)
    db.commit()


def get_user_match_history(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 5
):
    offset = (page - 1) * limit

    records = (
        db.query(MatchHistory)
        .filter(MatchHistory.user_id == user_id)
        .order_by(MatchHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    results = []

    for r in records:
        results.append({
            "id": r.id,
            "searched_skills": r.searched_skills.split(","),
            "match_count": r.match_count,
            "match_percentage": r.match_percentage,
            "score": r.score,
            "created_at": r.created_at
        })

    return results


def delete_all_history(db: Session, user_id: int):
    db.query(MatchHistory).filter(MatchHistory.user_id == user_id).delete()
    db.commit()


def delete_single_history(db: Session, user_id: int, record_id: int):
    record = db.query(MatchHistory).filter(
        MatchHistory.id == record_id,
        MatchHistory.user_id == user_id
    ).first()

    if record:
        db.delete(record)
        db.commit()
        return True

    return False


# ✅ NEW — EXPORT USER DATA
def export_user_data(db: Session, user: User):
    profile = {
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "skills": json.loads(user.skills) if user.skills else [],
        "created_at": user.created_at
    }

    history_records = (
        db.query(MatchHistory)
        .filter(MatchHistory.user_id == user.id)
        .order_by(MatchHistory.created_at.desc())
        .all()
    )

    history = []

    for r in history_records:
        history.append({
            "searched_skills": r.searched_skills.split(","),
            "match_count": r.match_count,
            "match_percentage": r.match_percentage,
            "score": r.score,
            "created_at": r.created_at
        })

    return {
        "profile": profile,
        "match_history": history
    }