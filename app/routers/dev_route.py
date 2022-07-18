

from fastapi import APIRouter

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
