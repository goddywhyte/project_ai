from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.database.database import engine
from app.database.base import Base
from app.routes.auth import router as auth_router
from app.routes.job import router as job_router
from app.routes.notification import router as notification_router
from app.routes.admin import router as admin_router
from app.middleware.rate_limiter import rate_limit

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def limiter(request: Request, call_next):
    rate_limit(request)
    return await call_next(request)


app.include_router(auth_router)
app.include_router(job_router)
app.include_router(notification_router)
app.include_router(admin_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Secure API running"}