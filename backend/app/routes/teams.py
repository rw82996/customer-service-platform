from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.audit import log_audit_event
from app.database import get_db
from app.models.team import Team
from app.schemas.team import (
    TeamCreate,
    TeamResponse,
    TeamUpdate,
    TeamWithMembersResponse,
)

router = APIRouter(prefix="/api/teams", tags=["Teams"])


@router.get("/", response_model=list[TeamResponse])
def list_teams(db: Session = Depends(get_db)):
    return db.query(Team).filter(Team.deleted_at.is_(None)).all()


@router.post("/", response_model=TeamResponse, status_code=201)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)):
    team = Team(**payload.model_dump())
    db.add(team)
    log_audit_event(
        db, action="create", entity_type="team", new_value=payload.model_dump()
    )
    db.commit()
    db.refresh(team)
    return team


@router.get("/{team_id}", response_model=TeamWithMembersResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id, Team.deleted_at.is_(None)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, payload: TeamUpdate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id, Team.deleted_at.is_(None)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    old_value = {
        "name": team.name,
        "description": team.description,
        "is_active": team.is_active,
    }
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(team, key, value)
    log_audit_event(
        db,
        action="update",
        entity_type="team",
        entity_id=team_id,
        old_value=old_value,
        new_value=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id, Team.deleted_at.is_(None)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.deleted_at = datetime.now(timezone.utc)
    log_audit_event(db, action="soft_delete", entity_type="team", entity_id=team_id)
    db.commit()
