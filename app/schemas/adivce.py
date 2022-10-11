from pydantic import BaseModel, UUID4
from enum import Enum
from datetime import datetime

class EmotionType(Enum):
  NEUTRAL='neutral'
  JOY='joy'
  SADNESS='sadness'
  SURPRISE='surprise'
  FEAR='fear'
  ANGER='anger'


class Advice(BaseModel):
    advice_id:UUID4
    emotion: EmotionType
    text: str
    is_deprecated: bool
    is_sender: bool

    class Config:
        orm_mode: True


class AdviceData(BaseModel): # не смотрел еще какие там поля извлекаются
  text: str
  emotion: str


class AdviceBody(BaseModel):
  advice_type: str = "emotion"
  data: AdviceData
  advice_id: UUID4


class AdvicePayload(BaseModel):
  chat_id: UUID4
  message_id: int
  user_id: UUID4
  advice: AdviceBody


class AdviceResponce(BaseModel):
  event_type: str = "advice"
  payload: AdvicePayload