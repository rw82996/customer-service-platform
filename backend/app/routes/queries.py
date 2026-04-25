from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.query import ClientQuery, QueryResponse
from app.schemas.query import (
    QueryCreate,
    QueryOut,
    QueryResponseCreate,
    QueryResponseOut,
    QueryUpdate,
    QueryWithResponsesOut,
)

router = APIRouter(prefix="/api/queries", tags=["Queries"])


@router.get("/", response_model=list[QueryOut])
def list_queries(
    status: str | None = None,
    priority: str | None = None,
    client_id: int | None = None,
    business_segment_id: int | None = None,
    assigned_staff_id: int | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(ClientQuery)
    if status:
        q = q.filter(ClientQuery.status == status)
    if priority:
        q = q.filter(ClientQuery.priority == priority)
    if client_id is not None:
        q = q.filter(ClientQuery.client_id == client_id)
    if business_segment_id is not None:
        q = q.filter(ClientQuery.business_segment_id == business_segment_id)
    if assigned_staff_id is not None:
        q = q.filter(ClientQuery.assigned_staff_id == assigned_staff_id)
    return q.order_by(ClientQuery.created_at.desc()).all()


@router.post("/", response_model=QueryOut, status_code=201)
def create_query(payload: QueryCreate, db: Session = Depends(get_db)):
    query = ClientQuery(**payload.model_dump())
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


@router.get("/{query_id}", response_model=QueryWithResponsesOut)
def get_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(ClientQuery).filter(ClientQuery.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return query


@router.patch("/{query_id}", response_model=QueryOut)
def update_query(query_id: int, payload: QueryUpdate, db: Session = Depends(get_db)):
    query = db.query(ClientQuery).filter(ClientQuery.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    update_data = payload.model_dump(exclude_unset=True)
    if update_data.get("status") == "resolved" and query.status != "resolved":
        update_data["resolved_at"] = datetime.now(timezone.utc)
    for key, value in update_data.items():
        setattr(query, key, value)
    db.commit()
    db.refresh(query)
    return query


@router.delete("/{query_id}", status_code=204)
def delete_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(ClientQuery).filter(ClientQuery.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    db.delete(query)
    db.commit()


@router.post("/{query_id}/responses", response_model=QueryResponseOut, status_code=201)
def add_response(query_id: int, payload: QueryResponseCreate, db: Session = Depends(get_db)):
    query = db.query(ClientQuery).filter(ClientQuery.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    response = QueryResponse(
        message=payload.message,
        is_internal_note=1 if payload.is_internal_note else 0,
        query_id=query_id,
        staff_id=payload.staff_id,
    )
    db.add(response)
    db.commit()
    db.refresh(response)
    return response


@router.get("/{query_id}/responses", response_model=list[QueryResponseOut])
def list_responses(query_id: int, db: Session = Depends(get_db)):
    return (
        db.query(QueryResponse)
        .filter(QueryResponse.query_id == query_id)
        .order_by(QueryResponse.created_at)
        .all()
    )
