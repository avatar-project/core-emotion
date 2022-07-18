

from typing import Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field


class UserTinySchema(BaseModel):
    user_id: UUID4


class UserGeneralSchema(BaseModel):
    user_id: UUID4 = Field(default_factory=uuid4)
    isu_id: str
    username: Optional[str]
    name: Optional[str] = ''
    middle_name: Optional[str] = ''
    last_name: Optional[str] = ''
