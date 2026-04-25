from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import analytics, business_segments, clients, queries, staff, teams

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Customer Service Platform",
    description="Manage client queries, team entitlements, and analytics across business segments",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(business_segments.router)
app.include_router(teams.router)
app.include_router(staff.router)
app.include_router(clients.router)
app.include_router(queries.router)
app.include_router(analytics.router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
