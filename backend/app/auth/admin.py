from fastapi import Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.models.user import User

# ⚠️ CHANGE THIS TO YOUR EMAIL
ADMIN_EMAIL = "your_email@gmail.com"


def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user