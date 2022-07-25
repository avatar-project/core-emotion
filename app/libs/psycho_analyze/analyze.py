from typing import List

from app.libs.emotion.emotion_detect import Emotion
from app.libs.mongo.psycho_crud import save_emotion_massage
from app.libs.toxic.bert_predict import BertPredict
from app.libs.toxic.mat_filter import count_mat_detect
from app.schemas.messages import EmotionSentBase, MessageBase, MessageWithEmotions
from nltk.tokenize import sent_tokenize


async def psycho_text_analyze(message: MessageBase):
    """Основная функция, в которой сообщения проходит весь пайплайн от предобработки и вычесления метрик до записи в базу и отправки пользователю

    Args:
        message (MessageBase): сообщение 
    """
    sents = await get_text_sents(message.text)  # Разбиваем сообщение на предложения
    # Анализируем каждое предложение
    emotion_list = await sents_get_psycho_metrics(sents)
    # Сохраняем каждое анализируемое предложение
    message_with_emotions = await message_get_psycho_metrics(message, emotion_list)
    await save_all_sents(message_with_emotions)

    return message_with_emotions


async def save_all_sents(message_with_emotions):
    """Save all sents of the message"""
    await save_emotion_massage(message_with_emotions)


async def message_get_psycho_metrics(message: MessageBase, emotion_list: EmotionSentBase) -> MessageWithEmotions:
    """Получаем психоэмоциональные метрики для полного текста сообщения, а также оборачиваем в схему все

    Args:
        message (MessageBase): сообщение    
        emotion_list (EmotionSentBase): список предложений с метриками

    Returns:
        MessageWithEmotions: сообщение с метриками и списком предложений с метриками
    """
    psycho_message = await get_psycho_metrics(message.text)

    message_with_emotions = MessageWithEmotions(
        **message.dict(),
        m_is_toxic=psycho_message['tox'],
        m_emotion=psycho_message['emo'],
        m_emotion_proba=psycho_message['emo_proba'],
        m_have_filthy=psycho_message['mat'],
        emotions=emotion_list
    )
    return message_with_emotions


async def calculate_coef(message_with_emotions: MessageWithEmotions):
    # TODO пересчет выбора эмоций и токсичности, с учетом эмоций по предложениям
    pass


async def get_advice():
    # TODO получить совет по коммуникации
    pass


async def sents_get_psycho_metrics(sents: List[str]) -> tuple:
    """Получить эмоцию, токсичность и наличие мата для каждого предложения сообщения

    Args:
        sents (List[str]): список предложений

    Returns:
        (List[EmotionSentBase]): список предложений с психоэмоциональными характеристиками
    """
    emotion_list = []

    for sent in sents:
        psycho = await get_psycho_metrics(sent)
        emotion_list.append(EmotionSentBase(
            text=sent,
            is_toxic=psycho['tox'],
            have_filthy=psycho['mat'],
            emotion=psycho['emo'],
            emotion_proba=psycho['emo_proba']
        ))

    return emotion_list


async def get_psycho_metrics(sent: str) -> dict:
    """Вычисляем психоэмоциональные метрики предложения 

    Args:
        sent (str): предложение

    Returns:
        dict: (emo: номер эмоции, emo_proba: вероятность эмоции, tox: токсичность, mat: нецензурная лексика)
    """
    emotion = Emotion()
    toxic = BertPredict()
    psycho = {}

    if len(sent.split()) < 3:
        psycho['emo'] = 0
        psycho['emo_proba'] = 1.0
        psycho['tox'] = False
    else:
        psycho['emo'], psycho['emo_proba'] = emotion.predict(sent)
        psycho['tox'] = toxic.predict(sent)

    psycho['mat'] = count_mat_detect(sent)[0]
    psycho['mat'] = True if psycho['mat'] else False

    return psycho


async def get_text_sents(text: str) -> List[str]:
    """Get all sentence from text message

    Args:
        text (str): message text

    Returns:
        List[str]: list og sentence
    """
    return sent_tokenize(text)
