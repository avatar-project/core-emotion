import random

from typing import List
from datetime import datetime, timedelta, timezone

from app.libs.emotion.emotion_detect import Emotion
from app.libs.toxic.mat_filter import count_mat_detect
from app.libs.toxic.toxic_detect import text2toxicity
from app.schemas.messages import Advice, EmotionType, MessageBase
from app.libs.postres_crud.queries import get_all_advices, get_user_emotion_a_message, get_last_user_advice_with_emotion, get_chat_users
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')


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
    """Расчитываем итоговую эмоцию, к эмоция по предложениям, добавляем эмоцию по всему сообщению. Затем находим наиболее часто встречаемую эмоцию,
    при равенстве эмоций, возвращаем эмоции по приоритету, грусть - радость - страх. При наличии токсичных сообщений, всегда решаем, что это злость.

    Args:
        message_with_emotion (dict): _description_
        sents_emotion_list (List[dict]): _description_

    Returns:
        EmotionType: _description_
    """
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
    # print(emotion_coeffs)
    for i, element in enumerate(emotion_coeffs):
        if element > max_coeffs:
            max_coeffs = element
            emotion_list = [i]
        elif element == max_coeffs:
            emotion_list.append(i)
    if max_coeffs == 0:
        return EmotionType.NEUTRAL
    emotion_dict = {
        0: 'neutral',
        1: 'joy',
        2: 'sadness',
        3: 'surprise',
        4: 'fear',
        5: 'anger'
    }
    emotion_value_list = []
    for emotion in emotion_list:
        emotion_value_list.append(emotion_dict[emotion])
    print(f'emotion_list {emotion_value_list}')

    if len(emotion_value_list) == 1:
        return EmotionType(emotion_value_list[0])
    elif EmotionType.SADNESS.value in emotion_value_list:
        return EmotionType.SADNESS
    elif EmotionType.JOY.value in emotion_value_list:
        return EmotionType.JOY
    elif EmotionType.FEAR.value in emotion_value_list:
        return EmotionType.FEAR

    return EmotionType.NEUTRAL


async def get_advice(message: MessageBase, message_emotion: EmotionType) -> List[Advice]:
    EMOTION_COUNT = 3

    users = await get_chat_users(message.message_id)  # Все пользователи которые относятся к этому сообщению
    # print(f'get_advice {message_emotion}')
    # Заполняем советы дефолтными None, если совета не будет
    advices_to_user = []
    for user in users:
        advices_to_user.append(
            Advice(
                user_id=user['user_id'],
                advice_id=None
            )
        )
    if message_emotion == EmotionType.NEUTRAL:
        return advices_to_user

    # Для отправителя получаем его сообщения в чате за последний час
    user_messages = await get_user_emotion_a_message(chat_id=message.chat_id,
                                                     user_id=message.user_id,
                                                     from_at=datetime.now(timezone.utc) - timedelta(hours=1),
                                                     to_at=datetime.now(timezone.utc))

    user_emotions = {}
    last_advice_message = None
    # print(f'user_message {user_messages}')
    # Смотрим, был ли совет за последний час, если по такой же эмоции был, то возвращаем дефолт
    for user_message in user_messages:

        if user_message['advice_id']:
            last_advice_message = user_message
            if user_message['emotion'].lower() == message_emotion.name.lower():
                return advices_to_user

        if user_emotions.get(user_message['emotion'].lower(), None):
            user_emotions[user_message['emotion'].lower()] += 1
        else:
            user_emotions[user_message['emotion'].lower()] = 1

    # Далее даем совет если текущая эмоция трижды встречалась за последний час или текущая эмоция встречалась больше раз, чем та, для которой дали уже совет
    current_emotion_count = user_emotions.get(message_emotion.name.lower(), 0)

    if last_advice_message:
        # print(f'last_advice_message: {current_emotion_count}')
        last_advice_emotion_count = user_emotions.get(last_advice_message['emotion'].lower(), 0)
        # print(last_advice_emotion_count)
        if current_emotion_count > EMOTION_COUNT and current_emotion_count >= last_advice_emotion_count:
            return await get_current_advice(message, message_emotion, users)
        else:
            return advices_to_user
    else:
        if current_emotion_count > EMOTION_COUNT:
            return await get_current_advice(message, message_emotion, users)
        else:
            return advices_to_user

    return advices_to_user


async def get_current_advice(message: MessageBase, message_emotion: EmotionType, users: List[dict]) -> List[Advice]:
    """
        Получаем текст совета для каждого пользователя
    """
    advicec = await get_all_advices()  # Получаем все советы

    users_advices = []

    # Пробегаем по юзерам и назначем каждому совет
    for i, user in enumerate(users):
        if user['user_id'] == message.user_id:
            # last_user_emotion_advice сюда записываем последний совет пользователю, чтобы не повторяться советами
            last_user_emotion_advice = await get_last_user_advice_with_emotion(
                user['user_id'], message_emotion.name.lower(), is_sender=True)

            # Ниже в suitable_advice фильтруем только подходящие советы для юзера
            if last_user_emotion_advice:
                suitable_advice = [x for x in advicec if x['emotion']
                                   == message_emotion.name.lower() and x['is_sender'] and x['advice_id'] != last_user_emotion_advice['advice_id']]
            else:
                suitable_advice = [x for x in advicec if x['emotion']
                                   == message_emotion.name.lower() and x['is_sender']]
        else:
            last_user_emotion_advice = await get_last_user_advice_with_emotion(
                user['user_id'], message_emotion.name.lower(), is_sender=False)

            if last_user_emotion_advice:
                suitable_advice = [x for x in advicec if x['emotion']
                                   == message_emotion.name.lower() and not x['is_sender'] and x['advice_id'] != last_user_emotion_advice['advice_id']]
            else:
                suitable_advice = [x for x in advicec if x['emotion']
                                   == message_emotion.name.lower() and not x['is_sender']]

        # и итоговый совет рандомом из подходящих
        random_index = random.randint(0, len(suitable_advice) - 1)

        users_advices.append(Advice(
            user_id=user['user_id'],
            advice_id=suitable_advice[random_index]['advice_id']
        ))

    return users_advices


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
