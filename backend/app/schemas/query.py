from datetime import datetime

from pydantic import BaseModel

from app.enums import QueryPriority, QueryStatus


class QueryCreate(BaseModel):
    subject: str
    description: str
    priority: QueryPriority = QueryPriority.MEDIUM
    category: str | None = None
    client_id: int
    business_segment_id: int | None = None
    assigned_staff_id: int | None = None


class QueryUpdate(BaseModel):
    subject: str | None = None
    description: str | None = None
    status: QueryStatus | None = None
    priority: QueryPriority | None = None
    category: str | None = None
    assigned_staff_id: int | None = None


class QueryResponseCreate(BaseModel):
    message: str
    is_internal_note: bool = False
    staff_id: int


class QueryResponseOut(BaseModel):
    id: int
    message: str
    is_internal_note: bool
    created_at: datetime
    query_id: int
    staff_id: int

    model_config = {"from_attributes": True}


class QueryOut(BaseModel):
    id: int
    subject: str
    description: str
    status: str
    priority: str
    category: str | None
    created_at: datetime
    updated_at: datetime | None
    resolved_at: datetime | None
    client_id: int
    business_segment_id: int | None
    assigned_staff_id: int | None

    model_config = {"from_attributes": True}


class QueryWithResponsesOut(QueryOut):
    responses: list[QueryResponseOut] = []


class PaginatedQueryResponse(BaseModel):
    items: list[QueryOut]
    total: int
    skip: int
    limit: int
