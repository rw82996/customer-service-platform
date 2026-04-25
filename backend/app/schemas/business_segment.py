from datetime import datetime

from pydantic import BaseModel


class BusinessSegmentCreate(BaseModel):
    name: str
    description: str | None = None


class BusinessSegmentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class BusinessSegmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
