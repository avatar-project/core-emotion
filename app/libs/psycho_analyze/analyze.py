from typing import List
from app.libs.emotion.emotion_detect import Emotion
from app.libs.toxic.bert_predict import BertPredict
from app.schemas.messages import MessageBase
from nltk.tokenize import sent_tokenize


async def psycho_text_analyze(message: MessageBase):
    """_summary_

    Args:
        message (MessageBase): _description_
    """
    sents = await get_text_sents(message.text)
    emotion = Emotion()
    toxic = BertPredict()

    emotion_list = []
    toxic_list = []
    for sent in sents:
        emo = emotion.predict(sent)
        emotion_list.append(emo)

        tox = toxic.predict(sent)
        toxic_list.append(tox)


async def get_text_sents(text: str) -> List[str]:
    """Get all sentence from text message

    Args:
        text (str): message text

    Returns:
        List[str]: list og sentence
    """
    return sent_tokenize(text)
