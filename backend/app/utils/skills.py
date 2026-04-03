import json


def normalize_skills(skills):
    if not skills:
        return None

    cleaned = []
    seen = set()

    for s in skills:
        name = s["name"].strip().lower()
        level = s["level"].lower()

        if (name, level) not in seen:
            cleaned.append({"name": name, "level": level})
            seen.add((name, level))

    return json.dumps(cleaned)


def skills_to_list(skills):
    if not skills:
        return []
    return json.loads(skills)