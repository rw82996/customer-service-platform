from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, nullable=True)

    business_segment_id = Column(
        Integer, ForeignKey("business_segments.id"), nullable=True
    )

    business_segment = relationship("BusinessSegment", back_populates="clients")
    queries = relationship("ClientQuery", back_populates="client")
    team_assignments = relationship("ClientTeamAssignment", back_populates="client")


class ClientTeamAssignment(Base):
    __tablename__ = "client_team_assignments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", back_populates="team_assignments")
    team = relationship("Team", back_populates="client_assignments")
