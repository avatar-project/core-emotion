from typing import List
from uuid import UUID
from platform_services.postgresql.injectors import async_session
from app.schemas.messages import MessageWithEmotions, MessageWithAdvice, SimpleAdvice, AdvicePayloadNew, AdviceBodyNew, AdviceDataNew
from app.schemas.adivce import Advice as AdviceSchema, AdviceBody, UserStateAdvanced, UserState
from app.pg_model.message_advice import MessageAdvice, Advice, UserStateModel
from app.rabbitmq.producer import mailer_advice
from pydantic import parse_obj_as
from sqlalchemy import select, update
from logging import getLogger


logger = getLogger("db-exeptions")


async def get_all_advices() -> List[dict]:
    """
    Получить все рекомендации
    """
    session = async_session()
    query = await session.execute("select * from advice")
    query = query.fetchall()
    await session.close()
    return query


async def get_user_emotion_a_message(chat_id, user_id, from_at, to_at) -> List[dict]:
    """
    Все сообщения пользователя в чате за промежуток времени от from_at до to_ad с эмоциями и советами если они есть.
    """

    sql_quary = """
    select ms.message_id, ms.user_id, ad.advice_id, ad.emotion from messages ms
        join message_advice ad on ms.message_id = ad.message_id and ms.user_id = ad.user_id
        where ms.chat_id = :chat_id
        and ms.user_id = :user_id
        and ms.created_at between :from_at
        and :to_at"""
    session = async_session()
    query = await session.execute(sql_quary, {"chat_id": chat_id, "user_id": user_id, "from_at": from_at.replace(tzinfo=None), "to_at": to_at.replace(tzinfo=None)})
    query = query.fetchall()
    await session.close()
    return query


async def get_last_user_advice_with_emotion(user_id, emotion: str, is_sender: bool):
    """
    Получить последний совет пользователя, с выбранной эмоцией (без привязки к чату), может вернуться None
    """
    sql_query = """
    select ma.user_id, ma.advice_id, ad.*  from message_advice ma
        join messages ms on ma.message_id = ms.message_id
        join advice ad on ad.advice_id = ma.advice_id
        where ma.user_id = :user_id
        and ad.emotion = :emotion
        and ad.is_sender = :is_sender
        order by ms.created_at desc
        limit 1"""
    session = async_session()
    query = await session.execute(sql_query, {"user_id": user_id, "emotion": emotion, "is_sender": is_sender})
    query = query.one_or_none()
    await session.close()
    return query


async def get_chat_users(message_id) -> List[dict]:
    """
    Получить id и имя пользователей в личном чате (Сейчас будут работать 
    только персональные чаты, при корректировке запроса смогут работать и групповые)
    """
    sql_query = """select u.user_id, u.username, u.firstname, u.lastname from messages ms
        join personal_chats pch on pch.chat_id = ms.chat_id
        join chat_user cu on cu.chat_id = pch.chat_id
        join users u on u.user_id = cu.user_id 
        where ms.message_id = :message_id
        """
    session = async_session()
    query = await session.execute(sql_query, {"message_id": message_id})
    query = query.fetchall()
    await session.close()
    return query


async def get_user_all_emotion_messages(user_id, from_at, to_at) -> List[dict]:
    """
    Все сообщения пользователя за промежуток времени от from_at до to_ad с эмоциями из всех чатов.
    """
    sql_query = """
        select ma.user_id, ms.chat_id, ms.created_at, ma.emotion, ma.advice_id  from message_advice ma
        join messages ms on ma.message_id = ms.message_id
        where ms.user_id = :user_id
        and ma.user_id = :user_id
        and ms.created_at between :from_at and :to_at
    """
    session = async_session()
    query = await session.execute(sql_query, {"user_id": user_id, "from_at": from_at, "to_at": to_at})
    query = query.fetchall()
    await session.close()
    return query


async def write_message_advice(message_advices: List[MessageWithEmotions]):
    async with async_session() as session:
        try:
            mass = [MessageAdvice(**advice.dict()) for advice in message_advices]
            session.add_all(mass)
            await session.commit()
            await session.flush()
        except Exception as e:
            logger.exception(f"WRITE message advice= {e}")
        # TODO проверить работу
        result = await session.execute(select(Advice.text, Advice.emotion, Advice.advice_id)
                                       .where(Advice.advice_id.in_((_advice.advice_id for _advice in message_advices))))

        # получаем текст совета
        advice_models: list = result.fetchall()

        # Перегоняем модели в схемы для удобства работы
        advice_schemas: List[MessageWithAdvice] = []

        # List ссылочный тип, это сво-во использую
        if len(advice_models) > 0:
            await send_emotion_with_advice(message_advices, advice_models, advice_schemas)
        else:
            await send_emotion_without_advice(message_advices, advice_schemas)
    await mailer_advice(advice_schemas)

# Надо рассмотреть рефакторинг/но работает быстрее чем через alchemy хз почему


async def send_emotion_without_advice(message_advices: List[MessageWithEmotions], advice_schemas: list):
    """Отправка сообщений с эмоцией но без совета"""
    for ms in message_advices:
        advice_schemas.append(
            AdvicePayloadNew(
                chat_id=ms.chat_id,
                message_id=ms.message_id,
                user_id=ms.user_id,
                advice=AdviceBodyNew(
                    advice_id=ms.advice_id,
                    data=AdviceDataNew(
                        text=None,
                        emotion=ms.emotion
                    )
                )
            )
        )

# Надо рассмотреть рефакторинг


async def send_emotion_with_advice(
        message_advices: List[MessageWithEmotions],
        advice_models: list,
        advice_schemas: list):
    """Отправка емоций, с советом"""
    for ms in message_advices:
        for ad in advice_models:
            if ms.advice_id == ad[-1]:
                advice_schemas.append(AdvicePayloadNew(
                    chat_id=ms.chat_id,
                    message_id=ms.message_id,
                    user_id=ms.user_id,
                    advice=AdviceBody(
                        advice_id=ms.advice_id,
                        data=AdviceDataNew(
                            text=ad[0],
                            emotion=ms.emotion
                        )
                    )
                ))


async def update_user_state(user_state: UserStateAdvanced):
    """Update user state table

    Args:
        user_state (UserStateAdvanced): _description_
    """
    async with async_session() as session:
        try:
            q = (
                update(UserStateModel)
                .where(UserStateModel.state_id == user_state.state_id)
                .values(state=user_state.state, importance=user_state.importance, recommender_id=user_state.recommender_id)
            )
            await session.execute(q)
            await session.commit()
        except Exception as e:
            logger.exception(f'UPDATE user state = {e}')


async def get_user_state(user_id, from_at, to_at) -> List[dict]:
    """
    Получить состояние пользователя за последние n дней
    """
    sql_query = """
        select ut.* from user_state ut
        where ut.user_id = :user_id
        and ut.date between :from_at and :to_at
        order by ut.date desc
    """
    session = async_session()
    query = await session.execute(sql_query, {"user_id": user_id, "from_at": from_at, "to_at": to_at})
    query = query.fetchall()
    await session.close()
    return query


async def get_user_last_state(user_id) -> dict:
    """
    Получить состояние пользователя за последние n дней
    """
    sql_query = """
        select ut.* from user_state ut
        where ut.user_id = :user_id
        order by ut.date desc
        limit 1
    """
    session = async_session()
    query = await session.execute(sql_query, {"user_id": user_id})
    query = query.one_or_none()
    await session.close()
    return query


async def write_user_state(user_state: UserState):
    """
        Сохранить состояние юзера в базу
    """
    async with async_session() as session:
        try:
            mass = UserStateModel(**user_state.dict())
            session.add(mass)
            await session.commit()
            await session.refresh(mass)
            state_id = mass.state_id
        except Exception as e:
            logger.exception(f"WRITE user state= {e}")

    return state_id


async def get_daily_state_recommender(emotion, category) -> List[dict]:
    """
    Получить советы по состоянию для нужной эмоции и категории.
    """
    sql_query = """
        select st.* from state_recommender st
        where st.emotion = :emotion
        and st.state_category = :category
    """
    session = async_session()
    query = await session.execute(sql_query, {"emotion": emotion, "category": category})
    query = query.fetchall()
    await session.close()
    return query
