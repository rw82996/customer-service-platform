from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.audit import log_audit_event
from app.database import get_db
from app.models.client import Client, ClientTeamAssignment
from app.schemas.client import (
    ClientCreate,
    ClientResponse,
    ClientTeamAssignmentCreate,
    ClientTeamAssignmentResponse,
    ClientUpdate,
)

router = APIRouter(prefix="/api/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientResponse])
def list_clients(
    business_segment_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    q = db.query(Client).filter(Client.deleted_at.is_(None))
    if business_segment_id is not None:
        q = q.filter(Client.business_segment_id == business_segment_id)
    return q.offset(skip).limit(limit).all()


@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**payload.model_dump())
    db.add(client)
    log_audit_event(
        db,
        action="create",
        entity_type="client",
        new_value=payload.model_dump(mode="json"),
    )
    db.commit()
    db.refresh(client)
    return client


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.deleted_at.is_(None))
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.deleted_at.is_(None))
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    old_value = {
        "name": client.name,
        "email": client.email,
        "company": client.company,
        "is_active": client.is_active,
    }
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    log_audit_event(
        db,
        action="update",
        entity_type="client",
        entity_id=client_id,
        old_value=old_value,
        new_value=payload.model_dump(exclude_unset=True, mode="json"),
    )
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.deleted_at.is_(None))
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.deleted_at = datetime.now(timezone.utc)
    log_audit_event(db, action="soft_delete", entity_type="client", entity_id=client_id)
    db.commit()


@router.post(
    "/assignments", response_model=ClientTeamAssignmentResponse, status_code=201
)
def assign_client_to_team(
    payload: ClientTeamAssignmentCreate, db: Session = Depends(get_db)
):
    assignment = ClientTeamAssignment(**payload.model_dump())
    db.add(assignment)
    log_audit_event(
        db,
        action="assign",
        entity_type="client_team_assignment",
        new_value=payload.model_dump(),
    )
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get(
    "/{client_id}/assignments", response_model=list[ClientTeamAssignmentResponse]
)
def get_client_assignments(client_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ClientTeamAssignment)
        .filter(ClientTeamAssignment.client_id == client_id)
        .all()
    )


@router.delete("/assignments/{assignment_id}", status_code=204)
def remove_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = (
        db.query(ClientTeamAssignment)
        .filter(ClientTeamAssignment.id == assignment_id)
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    log_audit_event(
        db,
        action="delete",
        entity_type="client_team_assignment",
        entity_id=assignment_id,
    )
    db.commit()
