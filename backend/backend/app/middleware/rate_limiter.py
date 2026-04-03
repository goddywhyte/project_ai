from fastapi import Request, HTTPException
import time

REQUEST_LOG = {}
LIMIT = 10
WINDOW = 60


def rate_limit(request: Request):
    ip = request.client.host
    now = time.time()

    if ip not in REQUEST_LOG:
        REQUEST_LOG[ip] = []

    REQUEST_LOG[ip] = [t for t in REQUEST_LOG[ip] if now - t < WINDOW]

    if len(REQUEST_LOG[ip]) >= LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests")

    REQUEST_LOG[ip].append(now)