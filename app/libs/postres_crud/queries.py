from typing import List
from platform_services.postgresql.injectors import async_session
from app.schemas.messages import MessageWithEmotions, MessageWithAdvice, SimpleAdvice
from app.schemas.adivce import Advice as AdviceSchema, AdviceBody
from app.pg_model.message_advice import MessageAdvice, Advice
from app.rabbitmq.producer import mailer_advice
from pydantic import parse_obj_as
from sqlalchemy import select

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
    select ma.user_id, ms.chat_id, ms.created_at, ma.advice_id, ad.*  from message_advice ma
        join messages ms on ma.message_id = ms.message_id
        join advice ad on ad.advice_id = ma.advice_id
        where ma.chat_id = '{}'
        and ma.user_id = '{}'
        and ms.created_at between '{}' 
        and '{}'""".format(
        chat_id, user_id, from_at, to_at
    )
    session = async_session()
    query = await session.execute(sql_quary)
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
        where ma.user_id = '{}'
        and ad.emotion = '{}'
        and ad.is_sender = {}
        order by ms.created_at desc
        limit 1""".format(
        user_id, emotion, is_sender
    )
    session = async_session()
    query = await session.execute(sql_query)
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
        where ms.message_id = {}
        """.format(
        message_id
    )

    session = async_session()
    query = await session.execute(sql_query)
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
        where ma.user_id = '{}'
        and ms.created_at between '{}' and '{}'
    """.format(
        user_id, from_at, to_at
    )
    session = async_session()
    query = await session.execute(sql_query)
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
            print(f"ERROR = {e}")
        #TODO проверить работу 
        print("GRABER",[_advice.advice_id for _advice in message_advices])
        result = await session.execute(select(Advice.text,Advice.emotion,Advice.advice_id)
                                .where(Advice.advice_id.in_((_advice.advice_id for _advice in message_advices))))
        advice_models:List[Advice] = result.fetchall()
        # Перегоняем модели в схемы для удобства работы
        advice_schemas:List[MessageWithAdvice] = []
        print(message_advices)
        print('___________________________')
        print(advice_models)
        for ms in message_advices:
            for ad in advice_models:
                if ms.advice_id == ad.advice_id:    
                    advice_schemas.append(MessageWithAdvice(
                        advice=AdviceBody(advice_id=ad.advice_id),
                        body=SimpleAdvice(text=ad.text, emotion=ad.emotion),
                        **ms.dict()))
        # advice_schemas = parse_obj_as(List[AdviceSchema], advice_models)
    await mailer_advice(advice_schemas)