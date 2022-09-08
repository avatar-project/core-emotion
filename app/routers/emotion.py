from fastapi import APIRouter
from app.libs.emotion.emotion_detect import Emotion
from app.libs.main import psycho_text_analyze

from app.libs.toxic.toxic_detect import text2toxicity
from app.libs.toxic.mat_filter import count_mat_detect
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
