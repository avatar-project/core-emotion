from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field
from app.libs.mongo.injectors import messages_collection
from app.schemas.messages import Destination, DestinationType

from app.settings import get_settings

settings = get_settings()


class SenderType(str, Enum):  # Тип отправителя
    USER = 'user',
    AVATAR = 'avatar'


class Message(BaseModel):
    message_id: UUID4 = Field(default_factory=uuid4)
    text: Optional[str] = ''
    sender_id: Optional[UUID4]
    sender_type: Optional[SenderType] = SenderType.USER
    destination: Destination
    timestamp: datetime = Field(default_factory=lambda: datetime.now(
        tz=timezone.utc))
    is_edit: bool = False
    read_by: List[UUID4] = []
    buttons_list: Optional[list[str]] = []


async def fill_database():
    """Функция для разработки, чисто чтобы забить базу тестовыми данными
    """
    items = [
        Message(
            text="Привет, рад тебя видеть",
            sender_id=UUID4('52233421-2e26-4f8a-bf5a-57ed61c0b299'),
            destination={
                'destination_id': UUID4('9f324c26-2725-41ba-9d2f-2bec019e21bb'),
                'type': DestinationType.USER
            },
            timestamp=datetime.now()
        ),

        Message(
            text="Как дела?",
            sender_id=UUID4('52233421-2e26-4f8a-bf5a-57ed61c0b299'),
            destination={
                'destination_id': UUID4('9f324c26-2725-41ba-9d2f-2bec019e21bb'),
                'type': DestinationType.USER
            },
            timestamp=datetime.now()
        ),

        Message(
            text="У меня все отлично",
            sender_id=UUID4('9f324c26-2725-41ba-9d2f-2bec019e21bb'),
            destination={
                'destination_id': UUID4('52233421-2e26-4f8a-bf5a-57ed61c0b299'),
                'type': DestinationType.USER
            },
            timestamp=datetime.now()
        ),

        Message(
            text="Я тебе расскажу как на меня напали. Я вчера шел ночью. И в подворотне на меня выскочил маньяк, я так испугался. Я сломал ногу, когда упал. Я ненавижу его теперь.",
            sender_id=UUID4('9f324c26-2725-41ba-9d2f-2bec019e21bb'),
            destination={
                'destination_id': UUID4('52233421-2e26-4f8a-bf5a-57ed61c0b299'),
                'type': DestinationType.USER
            },
            timestamp=datetime.now()
        ),

        Message(
            text="Смешно",
            sender_id=UUID4('52233421-2e26-4f8a-bf5a-57ed61c0b299'),
            destination={
                'destination_id': UUID4('9f324c26-2725-41ba-9d2f-2bec019e21bb'),
                'type': DestinationType.USER
            },
            timestamp=datetime.now()
        ),
    ]

    messages_col = messages_collection()
    await messages_col.insert_many((item.dict() for item in items))
