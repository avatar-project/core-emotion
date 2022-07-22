from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field


class DestinationType(str, Enum):  # тип получателя
    USER = 'user',
    CHANNEL = 'channel'


class Destination(BaseModel):  # получатель
    destination_id: UUID4
    type: DestinationType


class SenderType(str, Enum):  # Тип отправителя
    USER = 'user',
    AVATAR = 'avatar'


class EmotionType(int, Enum):
    NEUTRAL = 0,
    JOY = 1,
    SADNESS = 2,
    SURPRISE = 3,
    FEAR = 4,
    ANGER = 5


class MessageBase(BaseModel):
    message_id: UUID4
    text: str = ''
    sender_id: UUID4
    sender_type: Optional[SenderType]
    destination: Destination
    timestamp: datetime


class EmotionSentBase(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    text: str
    is_toxic: bool = False
    have_filthy: bool = False
    emotion: EmotionType = EmotionType.NEUTRAL
    emotion_proba: float = 1.0


class MessageWithEmotions(MessageBase):
    m_emotion: EmotionType = EmotionType.NEUTRAL
    m_emotion_proba: float = 1.0
    m_is_toxic: bool = False
    m_have_filthy: bool = False
    emotions: List[EmotionSentBase]
