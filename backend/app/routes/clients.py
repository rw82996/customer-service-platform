from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
    db: Session = Depends(get_db),
):
    q = db.query(Client)
    if business_segment_id is not None:
        q = q.filter(Client.business_segment_id == business_segment_id)
    return q.all()


@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()


@router.post("/assignments", response_model=ClientTeamAssignmentResponse, status_code=201)
def assign_client_to_team(payload: ClientTeamAssignmentCreate, db: Session = Depends(get_db)):
    assignment = ClientTeamAssignment(**payload.model_dump())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/{client_id}/assignments", response_model=list[ClientTeamAssignmentResponse])
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
    db.commit()
