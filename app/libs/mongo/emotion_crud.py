

from typing import List
from pydantic import UUID4
from app.libs.emotion.emotion_detect import Emotion
from app.libs.mongo.injectors import psycho_collection
from app.schemas.messages import EmotionMessageBase, MessageBase
from nltk.tokenize import sent_tokenize


async def psycho_text_analyze(message: MessageBase):
    """_summary_

    Args:
        message (MessageBase): _description_
    """
    print('hi')
    sents = await get_text_sents(message.text)
    emotion = Emotion()
    emotion_list = []
    for sent in sents:
        emo = emotion.predict(sent)
        emotion_list.append(emo)
    print(sents)
    print(emotion_list)


async def get_text_sents(text: str) -> List[str]:
    """Get all sentence from text message

    Args:
        text (str): message text

    Returns:
        List[str]: list og sentence
    """
    return sent_tokenize(text)


async def save_emotion_massage(emotion_message: EmotionMessageBase):
    """save message with emotion predict in the database

    Args:
        emotion_message (EmotionMessageBase): message
    """
    psycho_col = psycho_collection()

    await psycho_col.insert_one(emotion_message.dict())


async def get_message_info(message_id: UUID4) -> EmotionMessageBase:
    """Get information about message with emotion predict

    Args:
        message_id (UUID4): message id

    Returns:
        EmotionMessageBase: message with emotion
    """
    psycho_col = psycho_collection()

    message = await psycho_col.find_one({"message_id": message_id})

    if message:
        return EmotionMessageBase(**message)
