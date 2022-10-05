from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()

class MessageAdvice(Model):
    __tablename__ = "message_advice"

    user_id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    chat_id = Column(UUID(as_uuid=True), nullable=False)
    message_id = Column(Integer, nullable=False, primary_key=True)
    advice_id = Column(UUID(as_uuid=True))
    emotion = Column(ENUM('neutral','joy','sadness','surprise','fear','anger', name="EMOTION_TYPE"), nullable=False)


class Advice(Model):
    __tablename__ = "advice"
    advice_id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    emotion = Column(String, nullable=False)
    text = Column(String, nullable=False)
    is_deprecated = Column(Boolean)
    is_sender = Column(Integer)


