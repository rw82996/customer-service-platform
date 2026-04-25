from datetime import datetime

from pydantic import BaseModel


class QueryCreate(BaseModel):
    subject: str
    description: str
    priority: str = "medium"
    category: str | None = None
    client_id: int
    business_segment_id: int | None = None
    assigned_staff_id: int | None = None


class QueryUpdate(BaseModel):
    subject: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    category: str | None = None
    assigned_staff_id: int | None = None


class QueryResponseCreate(BaseModel):
    message: str
    is_internal_note: bool = False
    staff_id: int


class QueryResponseOut(BaseModel):
    id: int
    message: str
    is_internal_note: int
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
