

from typing import Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field

from app.schemas.messages import EmotionType


class UserTinySchema(BaseModel):
    user_id: UUID4


class UserAdvice(UserTinySchema):
    last_emotion: EmotionType
    last_angry_advice_num: int = 0
    last_fun_advice_num: int = 0
    last_sad_advice_num: int = 0
    last_fear_advice_num: int = 0
