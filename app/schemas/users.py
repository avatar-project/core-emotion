

from typing import Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field


class UserTinySchema(BaseModel):
    user_id: UUID4
