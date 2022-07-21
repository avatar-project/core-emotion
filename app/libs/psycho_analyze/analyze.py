from typing import List

from app.libs.emotion.emotion_detect import Emotion
from app.libs.toxic.bert_predict import BertPredict
from app.libs.toxic.mat_filter import count_mat_detect
from app.schemas.messages import EmotionMessageBase, MessageBase
from nltk.tokenize import sent_tokenize


async def psycho_text_analyze(message: MessageBase):
    """_summary_

    Args:
        message (MessageBase): _description_
    """
    emotion_sents = []

    sents = await get_text_sents(message.text)  # Разбиваем сообщение на предложения
    emotion_list, toxic_list, mat_list = await sents_get_psycho_metrics(sents)  # Анализируем каждое предложение
    for sent in sents:
        emotion_sents.append(
            EmotionMessageBase
        )


async def sents_get_psycho_metrics(sents: List[str]) -> tuple:
    """Получить эмоцию, токсичность и наличие мата для каждого предложения сообщения

    Args:
        sents (List[str]): список предложений

    Returns:
        tuple (List[int], List[bool], List[bool]): кортеж со списками для каждого предложения, эмоция, токсичность и мат
    """
    emotion_list = []
    toxic_list = []
    mat_list = []
    for sent in sents:
        emo, tox, mat = await get_psycho_metrics(sent)
        emotion_list.append(emo)
        toxic_list.append(tox)
        mat_list.append(mat)

    return emotion_list, toxic_list, mat_list


async def get_psycho_metrics(sent: str) -> tuple:
    emotion = Emotion()
    toxic = BertPredict()

    if len(sent.split()) < 2:
        emo = 0
        tox = False
    else:
        emo = emotion.predict(sent)[0]
        tox = toxic.predict(sent)

    mat = count_mat_detect(sent)[0]
    mat = True if mat else False

    return emo, tox, mat


async def get_text_sents(text: str) -> List[str]:
    """Get all sentence from text message

    Args:
        text (str): message text

    Returns:
        List[str]: list og sentence
    """
    return sent_tokenize(text)
