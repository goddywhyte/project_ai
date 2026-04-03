import json
from sqlalchemy.orm import Session

from app.models.user import User

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


def match_users_by_skills(db: Session, required_skills: list, min_match: int = 1):
    required_skills = [s.strip().lower() for s in required_skills]

    users = db.query(User).all()

    results = []

    for user in users:
        if not user.skills:
            continue

        user_skills = json.loads(user.skills)

        match_count = 0
        total_score = 0

        for req in required_skills:
            for s in user_skills:
                if s["name"] == req:
                    match_count += 1
                    total_score += LEVEL_SCORE.get(s["level"], 0)
                    break

        # ✅ Apply minimum match threshold
        if match_count >= min_match:
            final_score = (match_count * 10) + total_score

            results.append({
                "user": user,
                "score": final_score,
                "match_count": match_count
            })

    # Sort best matches first
    results.sort(key=lambda x: x["score"], reverse=True)

    return results