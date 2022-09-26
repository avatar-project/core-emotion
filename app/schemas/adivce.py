from tkinter import E
from pydantic import BaseModel, UUID4
from enum import Enum


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