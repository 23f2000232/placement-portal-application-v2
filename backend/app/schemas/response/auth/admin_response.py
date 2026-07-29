from uuid import UUID

from pydantic import BaseModel

from app.enums import UserRole


class AdminResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole