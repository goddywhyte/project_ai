from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.config.settings import APP_NAME
from app.database.database import engine
from app.database.base import Base
from app.routes.auth import router as auth_router
from app.utils.response import error_response
from app.utils.logger import get_logger

logger = get_logger("main")

app = FastAPI(title=APP_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail)
    )


@app.get("/")
def root():
    return {"message": f"{APP_NAME} is running"}