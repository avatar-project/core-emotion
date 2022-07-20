from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import UUID4, BaseModel


class DestinationType(str, Enum):  # тип получателя
    USER = 'user',
    CHANNEL = 'channel'


class Destination(BaseModel):  # получатель
    destination_id: UUID4
    type: DestinationType


class SenderType(str, Enum):  # Тип отправителя
    USER = 'user',
    AVATAR = 'avatar'


class EmotionType(str, Enum):
    NEUTRAL = 0,
    JOY = 1,
    SADNESS = 2,
    SURPRISE = 3,
    FEAR = 4,
    ANGER = 5


class MessageBase(BaseModel):
    message_id: UUID4
    text: Optional[str] = ''
    sender_id: Optional[UUID4]
    sender_type: Optional[SenderType]
    destination: Destination
    timestamp: datetime


class EmotionMessageBase(MessageBase):
    is_toxic: bool = False,
    have_filthy: bool = False,
    emotion: EmotionType = 0
