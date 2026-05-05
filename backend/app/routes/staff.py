from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.audit import log_audit_event
from app.auth import get_password_hash
from app.database import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffResponse, StaffUpdate

router = APIRouter(prefix="/api/staff", tags=["Staff"])


@router.get("/", response_model=list[StaffResponse])
def list_staff(team_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Staff).filter(Staff.deleted_at.is_(None))
    if team_id is not None:
        q = q.filter(Staff.team_id == team_id)
    return q.all()


@router.post("/", response_model=StaffResponse, status_code=201)
def create_staff(payload: StaffCreate, db: Session = Depends(get_db)):
    password_hash = get_password_hash(payload.password) if payload.password else None
    staff = Staff(
        name=payload.name,
        email=payload.email,
        password_hash=password_hash,
        role=payload.role.value,
        team_id=payload.team_id,
    )
    db.add(staff)
    log_audit_event(
        db,
        action="create",
        entity_type="staff",
        new_value={
            "name": payload.name,
            "email": payload.email,
            "role": payload.role.value,
        },
    )
    db.commit()
    db.refresh(staff)
    return staff


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = (
        db.query(Staff).filter(Staff.id == staff_id, Staff.deleted_at.is_(None)).first()
    )
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return staff


@router.patch("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, payload: StaffUpdate, db: Session = Depends(get_db)):
    staff = (
        db.query(Staff).filter(Staff.id == staff_id, Staff.deleted_at.is_(None)).first()
    )
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    old_value = {
        "name": staff.name,
        "email": staff.email,
        "role": staff.role,
        "is_active": staff.is_active,
    }
    update_data = payload.model_dump(exclude_unset=True)
    if "role" in update_data and update_data["role"] is not None:
        update_data["role"] = update_data["role"].value
    for key, value in update_data.items():
        setattr(staff, key, value)
    log_audit_event(
        db,
        action="update",
        entity_type="staff",
        entity_id=staff_id,
        old_value=old_value,
        new_value=payload.model_dump(exclude_unset=True, mode="json"),
    )
    db.commit()
    db.refresh(staff)
    return staff


@router.delete("/{staff_id}", status_code=204)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = (
        db.query(Staff).filter(Staff.id == staff_id, Staff.deleted_at.is_(None)).first()
    )
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    staff.deleted_at = datetime.now(timezone.utc)
    log_audit_event(db, action="soft_delete", entity_type="staff", entity_id=staff_id)
    db.commit()
