from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import ALLOWED_ORIGINS
from app.database import Base, engine, get_db
from app.logging_config import correlation_id_var, generate_correlation_id, logger
from app.routes import (
    analytics,
    auth,
    business_segments,
    clients,
    queries,
    staff,
    teams,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Service Platform",
    description="Manage client queries, team entitlements, and analytics across business segments",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Correlation-ID"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    cid = request.headers.get("X-Correlation-ID") or generate_correlation_id()
    correlation_id_var.set(cid)
    logger.info(f"{request.method} {request.url.path}")
    response: Response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    logger.info(f"{request.method} {request.url.path} -> {response.status_code}")
    return response


app.include_router(auth.router)
app.include_router(business_segments.router)
app.include_router(teams.router)
app.include_router(staff.router)
app.include_router(clients.router)
app.include_router(queries.router)
app.include_router(analytics.router)


@app.get("/api/health")
def health_check():
    db_healthy = True
    try:
        db: Session = next(get_db())
        db.execute("SELECT 1" if hasattr(db, "execute") else None)  # type: ignore
    except Exception:
        db_healthy = False
    return {
        "status": "healthy" if db_healthy else "degraded",
        "database": "connected" if db_healthy else "disconnected",
        "version": "2.0.0",
    }
