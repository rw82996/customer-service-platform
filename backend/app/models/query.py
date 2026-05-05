from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ClientQuery(Base):
    __tablename__ = "client_queries"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        String, nullable=False, default="open"
    )  # open, in_progress, resolved, closed
    priority = Column(
        String, nullable=False, default="medium"
    )  # low, medium, high, critical
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by = Column(Integer, nullable=True)

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    business_segment_id = Column(
        Integer, ForeignKey("business_segments.id"), nullable=True
    )
    assigned_staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)

    client = relationship("Client", back_populates="queries")
    business_segment = relationship("BusinessSegment", back_populates="queries")
    assigned_staff = relationship("Staff", foreign_keys=[assigned_staff_id])
    responses = relationship(
        "QueryResponse", back_populates="query", order_by="QueryResponse.created_at"
    )


class QueryResponse(Base):
    __tablename__ = "query_responses"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    is_internal_note = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    query_id = Column(Integer, ForeignKey("client_queries.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)

    query = relationship("ClientQuery", back_populates="responses")
    staff = relationship("Staff", back_populates="responses")
