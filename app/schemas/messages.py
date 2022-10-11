import datetime
from enum import Enum
from re import L
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

class SimpleAdvice(BaseModel):
    text :str
    emotion:str

class MessageWithAdvice(MessageWithEmotions):
    advice_type: str = "emotion"
    advice_id: Optional[UUID4]
    data: SimpleAdvice
    


#__________________________________________
class AdviceDataNew(BaseModel):
    text: Optional[str]
    emotion: str

class AdviceBodyNew(BaseModel):
    advice_type:str = "emotion"
    advice_id: Optional[UUID4]
    data: AdviceDataNew

class AdvicePayloadNew(BaseModel):
    chat_id: UUID4
    message_id: int
    user_id: UUID4
    advice: AdviceBodyNew

class AdviceResponceNew(BaseModel):
    event_type: str = "advice"
    payload: AdvicePayloadNew