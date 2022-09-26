from platform_services.postgresql import PostgreSQListener
from app.schemas.messages import MessageListener
from platform_services.postgresql.injectors import get_session, sessions, async_session

pl = PostgreSQListener()


@pl.listen_channel("/messenger/message/new")
async def listen_message(payload: MessageListener):
    session2 = async_session()
    query = await session2.execute("SELECT * FROM messages")
    print(query.fetchall())
    await session2.close()

