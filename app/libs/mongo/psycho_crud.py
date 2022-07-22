

from pydantic import UUID4
from app.libs.mongo.injectors import psycho_collection
from app.schemas.messages import EmotionSentBase


async def save_emotion_massage(emotion_message: EmotionSentBase):
    """Save message with emotion predict in the database

    Args:
        emotion_message (EmotionMessageBase): message
    """
    psycho_col = psycho_collection()

    await psycho_col.insert_one(emotion_message.dict())


async def get_message_info(message_id: UUID4) -> EmotionSentBase:
    """Get information about message with emotion predict

    Args:
        message_id (UUID4): message id

    Returns:
        EmotionMessageBase: message with emotion
    """
    psycho_col = psycho_collection()

    message = await psycho_col.find_one({"message_id": message_id})

    if message:
        return EmotionSentBase(**message)
