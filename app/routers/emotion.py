from datetime import datetime
from fastapi import APIRouter
from app.libs.emotion.emotion_detect import Emotion
from app.libs.main import change_user_state, get_daily_emotion, get_emotion_stat, get_last_state, get_recommender_variant, psycho_text_analyze
from pydantic import UUID4

from app.libs.toxic.toxic_detect import text2toxicity
from app.libs.toxic.mat_filter import count_mat_detect
from app.schemas.adivce import UserState, UserStateAdvanced
from app.schemas.messages import MessageBase

emotion_router = APIRouter()


@emotion_router.get(
    path='/',
    summary='Emotion'
)
async def index():
    return "Hi!"


@emotion_router.get(
    path='/is_toxic',
    summary='Is toxic text or not?',
    response_model=tuple
)
async def is_toxic(text: str):
    """
        <b>params:</b>
        text: str - text
        <br />
        <b>return:</b> - bool, True if text is toxic or False
    """
    toxic_proba = text2toxicity(text)
    if toxic_proba > 0.5:
        return (toxic_proba, True)
    else:
        return (toxic_proba, False)


@emotion_router.get(
    path='/mat_detect',
    summary='Подсчёт матерных слов',
    response_model=tuple
)
async def get_mat(text: str) -> tuple:
    """
    Подсчёт матерных слов

    :param text: Текст который нужно проанализировать задаётся как str. Может быть любой длины
    :type text: str
    :return: Возвращает кортеж. В первой ячейке которого содержится количество матерных слов, 
                                во второй - процент матерных слов в текста 
                                и в третьей - множество матерных слов.
    :rtype: tuple
    """
    return count_mat_detect(text)


@emotion_router.get(
    path='/get_emotion',
    summary='Определение эмоций'
)
async def emotion(text: str):
    emo = Emotion()
    return emo.predict(text)


# @emotion_router.post(
#     path='/psycho_text_analyze',
#     summary='Психоэмоциональный анализ сообщения'
# )
# async def text_analyze(message: MessageBase):
#     return await psycho_text_analyze(message)


@emotion_router.post(
    path='/text',
    summary='Психоэмоциональный анализ сообщения'
)
async def test(message: MessageBase):
    return await psycho_text_analyze(message)


@emotion_router.get(
    path='/get_emotion_stat',
    summary="Статистика по кол-ву эмоций в сообщениях за определенный промежуток времени",
    response_model=dict,
    response_description="dict: словарь {Эмоция: количество}"
)
async def emotion_stat(user_id: UUID4, from_at: datetime, to_at: datetime):
    return await get_emotion_stat(user_id, from_at, to_at)


@emotion_router.get(
    path='/get_daily_emotion',
    summary='Доминируящая за день эмоция',
    response_model=UserStateAdvanced,
    response_description='Схема с данными о состояние юзера'
)
async def daily_emotion(user_id: UUID4, chat_id: UUID4):
    return await get_daily_emotion(user_id, chat_id)


@emotion_router.post(
    path='change_user_state',
    summary='обновить инфу о состояние пользователя в базе'
)
async def change_user_state_p(user_state: UserStateAdvanced):
    await change_user_state(user_state)


@emotion_router.get(
    path='/get_recommender_variant',
    summary='получить кол-во дней с текущей (сегодняшней) эмоции',
    response_model=int,
    response_description='количество дней'
)
async def recommender_variant(user_id: UUID4):
    return await get_recommender_variant(user_id)


@emotion_router.get(
    path='/get_last_state',
    summary='Получить сегодняшнее состояние пользователя из БД',
    response_model=UserStateAdvanced,
    response_description='Схема с данными о состояние юзера'
)
async def last_state(user_id: UUID4):
    return await get_last_state(user_id)
