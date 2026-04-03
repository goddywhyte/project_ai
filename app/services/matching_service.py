from typing import List, Dict, Any, Optional
from app.utils.skills import normalize_skill
from app.utils.logger import logger


class MatchingService:

    LEVEL_HIERARCHY = {
        "beginner": 1,
        "intermediate": 2,
        "expert": 3
    }

    @staticmethod
    def match_users(
        users: List[Dict[str, Any]],
        required_skills: List[str],
        min_match: int = 1,
        min_level: str = "beginner",
        role: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Match users with:
        - Role filtering
        - Skill threshold
        - Skill gap
        - Explanation
        - Level filtering
        """

        normalized_required = [normalize_skill(s) for s in required_skills]
        required_level_value = MatchingService.LEVEL_HIERARCHY.get(min_level, 1)

        # ✅ STEP 21 — Normalize role
        normalized_role = normalize_skill(role) if role else None

        matched_users = []

        for user in users:

            # ✅ ROLE FILTERING
            user_role = normalize_skill(user.get("role", ""))

            if normalized_role and user_role != normalized_role:
                continue

            user_skills = user.get("skills", [])

            # Build skill map
            user_skill_map = {}
            for skill in user_skills:
                name = normalize_skill(skill.get("name"))
                level = skill.get("level", "beginner")
                level_value = MatchingService.LEVEL_HIERARCHY.get(level, 1)
                user_skill_map[name] = level_value

            matched = []
            missing_skills = []

            for req_skill in normalized_required:
                user_level = user_skill_map.get(req_skill)

                if user_level and user_level >= required_level_value:
                    matched.append(req_skill)
                else:
                    missing_skills.append(req_skill)

            match_count = len(matched)

            if match_count < min_match:
                continue

            total_required = len(normalized_required) or 1
            match_percentage = round((match_count / total_required) * 100, 2)

            score = MatchingService._calculate_score(user_skills, normalized_required)

            explanation = MatchingService._generate_explanation(
                match_percentage,
                missing_skills
            )

            matched_users.append({
                "user_id": user.get("id"),
                "role": user.get("role"),
                "match_count": match_count,
                "matched_skills": matched,
                "missing_skills": missing_skills,
                "match_percentage": match_percentage,
                "score": score,
                "explanation": explanation,
                "profile": user
            })

        ranked = sorted(
            matched_users,
            key=lambda x: x["score"],
            reverse=True
        )

        logger.info(f"{len(ranked)} users matched with role filtering")

        return ranked

    @staticmethod
    def _calculate_score(user_skills, required_skills) -> float:
        level_weight = {
            "beginner": 1,
            "intermediate": 2,
            "expert": 3
        }

        score = 0

        for skill in user_skills:
            name = normalize_skill(skill.get("name"))
            level = skill.get("level", "beginner")

            if name in required_skills:
                score += level_weight.get(level, 1)

        return score

    @staticmethod
    def _generate_explanation(match_percentage: float, missing_skills: List[str]) -> str:

        if match_percentage == 100:
            return "Excellent match. You have all required skills."

        if match_percentage >= 70:
            if missing_skills:
                return f"Strong match. Consider improving: {', '.join(missing_skills)}."
            return "Strong match."

        if match_percentage >= 40:
            if missing_skills:
                return f"Moderate match. Missing: {', '.join(missing_skills)}."
            return "Moderate match."

        if missing_skills:
            return f"Low match. Improve: {', '.join(missing_skills)}."

        return "Low match."