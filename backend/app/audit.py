import json
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Session

from app.database import Base


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    actor_id = Column(Integer, nullable=True)
    actor_email = Column(String, nullable=True)
    actor_role = Column(String, nullable=True)
    action = Column(String, nullable=False)  # create, update, delete, login, etc.
    entity_type = Column(String, nullable=False)  # client, query, staff, team, etc.
    entity_id = Column(Integer, nullable=True)
    old_value = Column(Text, nullable=True)  # JSON
    new_value = Column(Text, nullable=True)  # JSON
    ip_address = Column(String, nullable=True)
    correlation_id = Column(String, nullable=True)


def log_audit_event(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    actor_id: int | None = None,
    actor_email: str | None = None,
    actor_role: str | None = None,
    old_value: dict | None = None,
    new_value: dict | None = None,
    ip_address: str | None = None,
    correlation_id: str | None = None,
) -> AuditEvent:
    event = AuditEvent(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=actor_id,
        actor_email=actor_email,
        actor_role=actor_role,
        old_value=json.dumps(old_value) if old_value else None,
        new_value=json.dumps(new_value) if new_value else None,
        ip_address=ip_address,
        correlation_id=correlation_id,
    )
    db.add(event)
    return event
