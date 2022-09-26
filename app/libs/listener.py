from platform_services.postgresql import PostgreSQListener
from app.schemas.messages import MessageListener, MessageWithEmotions, MessageBase
from platform_services.postgresql.injectors import get_session, sessions, async_session
from app.libs.main import psycho_text_analyze

pl = PostgreSQListener()


@pl.listen_channel("messenger/message/new")
async def listen_message(payload: MessageListener):
    session2 = async_session()
    sql_query = """SELECT chat_id, message_id, user_id, created_at,content 
        FROM messages WHERE message_id = {} and chat_id='{}'""".format(payload.message_id,payload.chat_id)
    query = await session2.execute(sql_query)
    query = query.one_or_none()
    await session2.close()
    await psycho_text_analyze(query)


# @pl.listen_channel("messenger/advice/new")
# async def listen_message(payload: str):
#     print(payload)
    # session2 = async_session()
    # query = await session2.execute("SELECT * FROM messages")
    # print(query.fetchall())
    # await session2.close()
