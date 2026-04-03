import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

# ✅ IMPORT YOUR EXISTING MODULES
from app.database.base import Base
from app.database.session import engine

from app.routes.auth import router as auth_router
from app.routes.job import router as job_router
from app.routes.notification import router as notification_router
from app.routes.admin import router as admin_router

from app.middleware.rate_limit import rate_limit


# ✅ CREATE APP
app = FastAPI()


# ✅ CREATE DATABASE TABLES
Base.metadata.create_all(bind=engine)


# ✅ MIDDLEWARE
@app.middleware("http")
async def limiter(request: Request, call_next):
    rate_limit(request)
    response = await call_next(request)
    return response


# ✅ ROUTES
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(notification_router)
app.include_router(admin_router)


# ✅ FIXED UPLOADS DIRECTORY (VERY IMPORTANT)
UPLOAD_DIR = os.path.join(os.getcwd(), "backend", "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# ✅ ROOT ENDPOINT
@app.get("/")
def root():
    return {"message": "Secure API running"}