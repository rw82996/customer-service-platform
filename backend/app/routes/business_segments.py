from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.audit import log_audit_event
from app.database import get_db
from app.models.business_segment import BusinessSegment
from app.schemas.business_segment import (
    BusinessSegmentCreate,
    BusinessSegmentResponse,
    BusinessSegmentUpdate,
)

router = APIRouter(prefix="/api/business-segments", tags=["Business Segments"])


@router.get("/", response_model=list[BusinessSegmentResponse])
def list_segments(db: Session = Depends(get_db)):
    return db.query(BusinessSegment).filter(BusinessSegment.deleted_at.is_(None)).all()


@router.post("/", response_model=BusinessSegmentResponse, status_code=201)
def create_segment(payload: BusinessSegmentCreate, db: Session = Depends(get_db)):
    segment = BusinessSegment(**payload.model_dump())
    db.add(segment)
    log_audit_event(
        db,
        action="create",
        entity_type="business_segment",
        new_value=payload.model_dump(),
    )
    db.commit()
    db.refresh(segment)
    return segment


@router.get("/{segment_id}", response_model=BusinessSegmentResponse)
def get_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = (
        db.query(BusinessSegment)
        .filter(BusinessSegment.id == segment_id, BusinessSegment.deleted_at.is_(None))
        .first()
    )
    if not segment:
        raise HTTPException(status_code=404, detail="Business segment not found")
    return segment


@router.patch("/{segment_id}", response_model=BusinessSegmentResponse)
def update_segment(
    segment_id: int, payload: BusinessSegmentUpdate, db: Session = Depends(get_db)
):
    segment = (
        db.query(BusinessSegment)
        .filter(BusinessSegment.id == segment_id, BusinessSegment.deleted_at.is_(None))
        .first()
    )
    if not segment:
        raise HTTPException(status_code=404, detail="Business segment not found")
    old_value = {
        "name": segment.name,
        "description": segment.description,
        "is_active": segment.is_active,
    }
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(segment, key, value)
    log_audit_event(
        db,
        action="update",
        entity_type="business_segment",
        entity_id=segment_id,
        old_value=old_value,
        new_value=payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(segment)
    return segment


@router.delete("/{segment_id}", status_code=204)
def delete_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = (
        db.query(BusinessSegment)
        .filter(BusinessSegment.id == segment_id, BusinessSegment.deleted_at.is_(None))
        .first()
    )
    if not segment:
        raise HTTPException(status_code=404, detail="Business segment not found")
    segment.deleted_at = datetime.now(timezone.utc)
    log_audit_event(
        db, action="soft_delete", entity_type="business_segment", entity_id=segment_id
    )
    db.commit()
