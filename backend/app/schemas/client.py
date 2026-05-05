from datetime import datetime

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None
    phone: str | None = None
    business_segment_id: int | None = None


class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    company: str | None = None
    phone: str | None = None
    business_segment_id: int | None = None
    is_active: bool | None = None


class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    company: str | None
    phone: str | None
    is_active: bool
    business_segment_id: int | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class ClientTeamAssignmentCreate(BaseModel):
    client_id: int
    team_id: int


class ClientTeamAssignmentResponse(BaseModel):
    id: int
    client_id: int
    team_id: int
    assigned_at: datetime

    model_config = {"from_attributes": True}
