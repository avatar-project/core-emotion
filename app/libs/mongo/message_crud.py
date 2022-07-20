
from datetime import datetime, date
from typing import List
from pydantic import UUID4

from app.libs.mongo.injectors import messages_collection
from app.schemas.messages import MessageBase


async def get_user_day_messages(user_id: UUID4) -> List[MessageBase]:
    """Get last day user messages

    Args:
        user_id (UUID4): user UUID4

    Returns:
        List[MessageBase]: Messages
    """
    current_date = date.today()

    start_timestamp = datetime(current_date.year, current_date.month, current_date.day-1, 22, 0, 0)
    end_timestamp = datetime(current_date.year, current_date.month, current_date.day, 22, 0, 0)

    return await get_user_messages(user_id, start_timestamp, end_timestamp)


async def get_user_messages(user_id: UUID4, start_timestamp: datetime, end_timestamp: datetime) -> List[MessageBase]:
    """Получить сообщения пользователя за определенный период

    Args:
        user_id (UUID4): [пользователь]
        start_timestamp (datetime): [От какой datetime]
        end_timestamp (datetime): [По какой datetime]

    Returns:
        List[MessageBase]: [Список сообщений пользователя]
    """
    messages_col = messages_collection()

    messages_list = messages_col.find({'sender_id': user_id, 'timestamp': {'$gte': start_timestamp}})

    return [MessageBase(**message) async for message in messages_list]
