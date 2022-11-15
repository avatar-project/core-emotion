from datetime import date, datetime, timedelta
from pydantic import UUID4

from app.libs.psycho_analyze.analyze import (
    calculate_coef,
    get_advice,
    get_text_sents,
    message_get_psycho_metrics,
    sents_get_psycho_metrics)
from app.pg_model.message_advice import UserStateModel
from app.schemas.adivce import EmotionType, StateRecommender, UserState, UserStateAdvanced
from app.schemas.messages import MessageBase, MessageWithEmotions
from app.libs.psycho_analyze.daily_analyze import choice_text_recommendation, get_date_emotion_count, main_emotion, recommender_variant
from app.libs.postres_crud.queries import get_user_state, update_user_state, write_message_advice, write_user_state


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

    await write_message_advice(message_with_emotion)


async def get_daily_emotion_stat(user_id: UUID4, from_at: date, to_at: date) -> list:
    """Получить ежедневные эмоции пользователя за определенный период

    Args:
        user_id (UUID4): _description_
        from_at (date): с какой даты
        to_at (date): по какую

    Returns:
        list: _description_
    """
    user_states = []
    user_states_dict = await get_user_state(user_id, from_at, to_at)
    for user_state in user_states_dict:
        user_states.append(UserStateAdvanced(**user_state))
    return user_states


async def get_emotion_stat(user_id: UUID4, from_at: datetime, to_at: datetime) -> dict:
    """Статистика по кол-ву эмоций в сообщениях за определенный промежуток времени

    Args:
        user_id (UUID4): _description_
        from_at (datetime): _description_
        to_at (datetime): _description_

    Returns:
        dict: словарь {Эмоция: количество}
    """

    emotion_counts = await get_date_emotion_count(user_id, from_at, to_at)

    if not emotion_counts:
        return None

    return emotion_counts


async def get_daily_emotion(user_id: UUID4, chat_id: UUID4) -> UserStateAdvanced:
    """для какой эмоции давать совет в этот день

    Args:
        user_id (UUID4): user id

    Returns:
        _type_: _description_
    """
    daily_emotion = await main_emotion(user_id)

    user_state = UserState(
        user_id=user_id,
        chat_id=chat_id,
        state=daily_emotion,
        date=date.today()
    )

    state_id = await write_user_state(user_state)

    user_state_advanced = UserStateAdvanced(
        **user_state.dict(),
        state_id=state_id
    )

    return user_state_advanced


async def change_user_state(user_state: UserStateAdvanced):
    """Обновляем в базе состояние пользователя в зависимости от его ответов

    Args:
        user_state (UserStateAdvanced): _description_
    """
    await update_user_state(user_state)


async def get_recommender_variant(user_id: UUID4) -> int:
    """Сколько дней подряд последнее (текущее) состояние пользователя идет

    Args:
        user_id (UUID4): _description_

    Returns:
        int: дней подряд
    """
    return await recommender_variant(user_id)


async def get_today_state(user_id: UUID4) -> UserStateAdvanced:
    """Получить сегодняшнее состояние пользователя

    Args:
        user_id (UUID4): _description_

    Returns:
        UserStateAdvanced: _description_
    """
    user_state = await get_user_state(user_id, date.today(), date.today())
    if user_state:
        return UserStateAdvanced(**user_state[0])
    else:
        return None


async def get_text_recommender(user_id: UUID4, emotion: EmotionType, state_category: int) -> StateRecommender:
    """Получить совет на основе эмоции и категории (насколько сильно проявляется эмоция)    

    Args:
        user_id (UUID4): _description_
        emotion (EmotionType): _description_
        state_category (int): _description_

    Returns:
        _type_: _description_
    """
    recommendation = await choice_text_recommendation(user_id=user_id, emotion=emotion, state_category=state_category)
    return recommendation
