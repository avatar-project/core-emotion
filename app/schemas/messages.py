import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field
from datetime import datetime


class EmotionType(int, Enum):
    NEUTRAL = 0,
    JOY = 1,
    SADNESS = 2,
    SURPRISE = 3,
    FEAR = 4,
    ANGER = 5


class MessageBase(BaseModel):
    chat_id: UUID4
    message_id: UUID4
    created_at: datetime
    content: str = ''


class Advice(BaseModel):
    advice_sender: Optional[str]
    advice_recipient: Optional[str]


class MessageWithEmotions(BaseModel):
    message_id: UUID4
    emotion: EmotionType
    advice: Advice
