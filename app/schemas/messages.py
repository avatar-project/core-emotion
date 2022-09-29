import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field
from datetime import datetime


class EmotionType(Enum):
  NEUTRAL='neutral'
  JOY='joy'
  SADNESS='sadness'
  SURPRISE='surprise'
  FEAR='fear'
  ANGER='anger'


class MessageBase(BaseModel):
    chat_id: UUID4
    message_id: int
    user_id: UUID4
    created_at: datetime
    content: str = ''


class Advice(BaseModel):
    user_id: UUID4
    advice_id: Optional[UUID4]


class MessageWithEmotions(BaseModel):
    chat_id: UUID4
    user_id: UUID4
    message_id: int
    emotion: str
    advice_id: Optional[UUID4]


class MessageListener(BaseModel):
    message_id: int
    chat_id: UUID4

