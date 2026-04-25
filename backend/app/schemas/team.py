from datetime import datetime

from pydantic import BaseModel

from app.schemas.staff import StaffResponse


class TeamCreate(BaseModel):
    name: str
    description: str | None = None


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class TeamResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class TeamWithMembersResponse(TeamResponse):
    members: list[StaffResponse] = []
