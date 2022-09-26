from typing import List
from platform_services.postgresql.injectors import async_session

async def get_all_advices() -> List[dict]:
    """
        create sql query to get advices
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
        and '{}'""".format(chat_id,user_id,from_at,to_at)
    session = async_session()
    query = await session.execute(sql_quary)
    query = query.fetchall()
    await session.close()
    return query
    


async def get_last_user_advice_with_emotion(user_id, emotion: str, is_sender: bool) :
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
        limit 1""".format(user_id,emotion,is_sender)
    session = async_session()
    query = await session.execute(sql_query)
    query = query.one_or_none()
    await session.close()
    return query

async def get_chat_users(message_id)-> List[dict]:
    """
    Получить id и имя пользователей в личном чате
    """
    sql_query = """select u.user_id, u.username, u.firstname, u.lastname from messages ms
        join users u on ms.user_id = u.user_id
        where ms.message_id = {}""".format(message_id)

    session = async_session()
    query = await session.execute(sql_query)
    query = query.fetchall()
    await session.close()
    return query



async def get_user_all_emotion_messages(user_id, from_at, to_at) -> List[dict]:
    """
        Все сообщения пользователя за промежуток времени от from_at до to_ad с эмоциями из всех чатов.
    """
    sql_query="""
        select ma.user_id, ms.chat_id, ms.created_at, ma.emotion, ma.advice_id  from message_advice ma
        join messages ms on ma.message_id = ms.message_id
        where ma.user_id = '{}'
        and ms.created_at between '{}' and '{}'
    """.format(user_id,from_at,to_at)
    session = async_session()
    query = await session.execute(sql_query)
    query = query.fetchall()
    await session.close()
    return query