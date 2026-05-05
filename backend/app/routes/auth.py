from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import Token, create_access_token, get_password_hash, verify_password
from app.audit import log_audit_event
from app.database import get_db
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    staff = (
        db.query(Staff)
        .filter(
            Staff.email == form_data.username,
            Staff.is_active.is_(True),
            Staff.deleted_at.is_(None),
        )
        .first()
    )

    if (
        not staff
        or not staff.password_hash
        or not verify_password(form_data.password, staff.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": staff.id, "email": staff.email, "role": staff.role}
    )
    log_audit_event(
        db,
        action="login",
        entity_type="staff",
        entity_id=staff.id,
        actor_id=staff.id,
        actor_email=staff.email,
    )
    db.commit()
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=StaffResponse, status_code=201)
def register(payload: StaffCreate, db: Session = Depends(get_db)):
    existing = db.query(Staff).filter(Staff.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

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
        db, action="register", entity_type="staff", actor_email=payload.email
    )
    db.commit()
    db.refresh(staff)
    return staff
