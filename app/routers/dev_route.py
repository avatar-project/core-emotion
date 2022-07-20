

from fastapi import APIRouter
from pydantic import UUID4
from app.libs.mongo.message_crud import get_user_day_messages

from app.libs.mongo.user_crud import get_all_users


dev_router = APIRouter()


@dev_router.get(
    path='/',
    summary='Emotion'
)
async def index():
    return "Hi!"


@dev_router.get(
    path='/all_users'
)
async def all_users():
    return await get_all_users()


@dev_router.get(
    path='/get_user_messages'
)
async def get_user_messages(user_id: UUID4):
    # Просто тестим получение сообщений о пользователе
    return await get_user_day_messages(user_id)
