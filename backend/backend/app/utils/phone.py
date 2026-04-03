import re
from fastapi import HTTPException


def normalize_phone(phone: str):
    if not phone.startswith("+"):
        raise HTTPException(status_code=400, detail="Must include country code")

    phone = phone.replace(" ", "")

    if not re.fullmatch(r"\+\d{7,15}", phone):
        raise HTTPException(status_code=400, detail="Invalid phone")

    return phone