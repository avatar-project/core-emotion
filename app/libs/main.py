from datetime import datetime
from pydantic import UUID4

from app.libs.psycho_analyze.analyze import (
    calculate_coef,
    get_advice,
    get_text_sents,
    message_get_psycho_metrics,
    sents_get_psycho_metrics)
from app.schemas.messages import MessageBase, MessageWithEmotions
from app.libs.psycho_analyze.daily_analyze import get_date_emotion_count, main_emotion
from app.libs.postres_crud.queries import write_message_advice


async def psycho_text_analyze(message: MessageBase):
    """Основная функция, в которой сообщения проходит весь пайплайн предобработки и вычесления метрик 

    Args:
        message (MessageBase): сообщение 
    """
    sents = await get_text_sents(message.content)  # Разбиваем сообщение на предложения
    # Анализируем каждое предложение
    sents_emotion_list = await sents_get_psycho_metrics(sents)
    # Анализируем все предложение
    message_with_emotion = await message_get_psycho_metrics(message)
    # Находим итоговую эмоцию для сообщения
    message_emotion = await calculate_coef(message_with_emotion, sents_emotion_list)
    # Получаем совет
    advices = await get_advice(message, message_emotion)
    # print("###"*30)
    # готовим данные к возврату
    message_with_emotion = []
    # print(advices)
    for advice in advices:
        message_with_emotion.append(
            MessageWithEmotions(
                chat_id=message.chat_id,
                user_id=advice.user_id,
                message_id=message.message_id,
                emotion=message_emotion.name.lower(),
                advice_id=advice.advice_id
            )
        )
    # Запись в базу
    # print(message_with_emotion)
    await write_message_advice(message_with_emotion)


async def get_emotion_stat(user_id: UUID4, from_at: datetime, to_at: datetime):
    """Статистика по кол-ву эмоций в сообщениях за определенный промежуток времени

    Args:
        user_id (UUID4): _description_
        from_at (datetime): _description_
        to_at (datetime): _description_

    Returns:
        _type_: _description_
    """

    emotion_counts = await get_date_emotion_count(user_id, from_at, to_at)

    if not emotion_counts:
        return None

    await emotion_counts


async def get_daily_emotion(user_id: UUID4) -> str:
    """для какой эмоции давать совет в этот день

    Args:
        user_id (UUID4): user id

    Returns:
        _type_: _description_
    """
    daily_emotion = await main_emotion()
    # TODO сохранение ежедневной эмоции в базу
    return daily_emotion


async def change_daily_emotion(user_id: UUID4, new_emotion: str):
    # TODO менять ежедневное состояние пользователя в базе
    ...


async def recommender_variant():
    # TODO посчитать сколько дней подряд эта эмоция, для выбора замера
    ...
