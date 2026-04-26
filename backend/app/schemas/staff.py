from datetime import datetime

from pydantic import BaseModel, EmailStr


class StaffCreate(BaseModel):
    name: str
    email: str
    role: str = "agent"
    team_id: int | None = None


class StaffUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None
    team_id: int | None = None
    is_active: bool | None = None


class StaffResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    team_id: int | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
