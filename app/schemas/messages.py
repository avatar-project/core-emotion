from enum import Enum
from typing import Optional
from pydantic import UUID4, BaseModel


class DestinationType(str, Enum):  # тип получателя
    USER = 'user',
    CHANNEL = 'channel'


class Destination(BaseModel):  # получатель
    destination_id: UUID4
    type: DestinationType


class MessageBase(BaseModel):
    text: Optional[str] = ''
    sender_id: Optional[UUID4]
    destination: Destination
