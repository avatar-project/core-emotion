from typing import List

from app.libs.emotion.emotion_detect import Emotion
from app.libs.toxic.mat_filter import count_mat_detect
from app.libs.toxic.toxic_detect import text2toxicity
from app.schemas.messages import Advice, EmotionType, MessageBase
from nltk.tokenize import sent_tokenize



async def message_get_psycho_metrics(message: MessageBase) -> dict:
    """Получаем психоэмоциональные метрики для полного текста сообщения, а также оборачиваем в схему все

    Args:
        message (MessageBase): сообщение    

    Returns:
        dict: {emotion: эмоция, emotion_proba: вероятность эмоции, toxic: токсичность, toxic_proba: вероятность токсичности, 
                filthy: нецензурная лексика, filthy_count: кол-во нецензурной лексика}
    """
    psycho_message = await get_psycho_metrics(message.content)

    return psycho_message


async def calculate_coef(message_with_emotion: dict, sents_emotion_list: List[dict]) -> EmotionType:
    sents_emotion_list.append(message_with_emotion)

    coef = {
        'toxic_count': 0,
        'non_toxic_count': 0
    }

    emotion_coeffs = [0]*6

    for element in sents_emotion_list:
        if element['toxic']:
            coef['toxic_count'] += 1
        else:
            coef['non_toxic_count'] += 1
        if element['emotion']:
            emotion_coeffs[element['emotion']] += 1

    if coef['toxic_count'] > 0:
        return EmotionType.ANGER

    max_coeffs = 0
    emotion_list = []
    print(emotion_coeffs)
    for i, element in enumerate(emotion_coeffs):
        if element > max_coeffs:
            max_coeffs = element
            emotion_list = [i]
        elif element == max_coeffs:
            emotion_list.append(i)
    if max_coeffs == 0:
        return EmotionType.NEUTRAL

    if len(emotion_list) == 1:
        return EmotionType(emotion_list[0])
    elif EmotionType.SADNESS.value in emotion_list:
        return EmotionType.SADNESS
    elif EmotionType.JOY.value in emotion_list:
        return EmotionType.JOY
    elif EmotionType.FEAR.value in emotion_list:
        return EmotionType.FEAR

    return EmotionType.NEUTRAL


async def get_advice(message: MessageBase, message_emotion: EmotionType):
    # TODO получить совет по коммуникации
    return Advice(advice_sender='В твоих сообщениях я увидел много раздражения. Может быть, стоит успокоиться и вернуться к переписке позже?',
            advice_recipient='Я определил, что Name нервничает. Попробуй уточнить причины его состояния.')


async def sents_get_psycho_metrics(sents: List[str]) -> List[dict]:
    """Получить эмоцию, токсичность и наличие мата для каждого предложения сообщения

    Args:
        sents (List[str]): список предложений

    Returns:
        (List[EmotionSentBase]): список предложений с психоэмоциональными характеристиками
    """
    emotion_list = []

    for sent in sents:
        psycho = await get_psycho_metrics(sent)
        emotion_list.append(psycho)

    return emotion_list


async def get_psycho_metrics(sent: str) -> dict:
    """Вычисляем психоэмоциональные метрики предложения 

    Args:
        sent (str): предложение

    Returns:
        dict: (emotion: эмоция, emotion_proba: вероятность эмоции, toxic: токсичность, toxic_proba: вероятность токсичности, 
                filthy: нецензурная лексика, filthy_count: кол-во нецензурной лексика)
    """
    emotion = Emotion()
    psycho = {}

    if len(sent.split()) < 3:
        psycho['emotion'] = 0
        psycho['emotion_proba'] = 1.0
        psycho['toxic'] = False
        psycho['toxic_proba'] = 0.0
    else:
        psycho['emotion'], psycho['emotion_proba'] = emotion.predict(sent)
        toxic_proba = text2toxicity(sent)
        psycho['toxic_proba'] = toxic_proba
        if toxic_proba > 0.5:
            psycho['toxic'] = True
        else:
            psycho['toxic'] = False

    psycho['filthy_count'] = count_mat_detect(sent)[0]
    psycho['filthy'] = True if psycho['filthy_count'] else False

    return psycho


async def get_text_sents(text: str) -> List[str]:
    """Get all sentence from text message

    Args:
        text (str): message text

    Returns:
        List[str]: list og sentence
    """
    return sent_tokenize(text)
