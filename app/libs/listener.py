from platform_services.postgresql import PostgreSQListener
from app.schemas.messages import MessageListener, MessageWithEmotions, MessageBase
from platform_services.postgresql.injectors import async_session
from app.libs.main import psycho_text_analyze

pl = PostgreSQListener()


@pl.listen_channel("/messenger/message/new")
async def listen_message(payload: MessageListener):
    session2 = async_session()
    sql_query = """SELECT ms.chat_id, ms.message_id, ms.user_id, ms.created_at,ms.content FROM messages ms
        join personal_chats pch on pch.chat_id = ms.chat_id
        WHERE ms.message_id = {} and 
        ms.chat_id='{}'""".format(payload.message_id,payload.chat_id)
    query = await session2.execute(sql_query)
    query = query.one_or_none()
    if query is not None:
        await session2.close()
        await psycho_text_analyze(query)
