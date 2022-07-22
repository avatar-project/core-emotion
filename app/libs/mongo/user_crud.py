

from typing import List
from app.libs.mongo.injectors import users_collection
from app.schemas.users import UserTinySchema


async def get_all_users() -> List[UserTinySchema]:

    users_col = users_collection()

    users = users_col.find({})
    users = [UserTinySchema(**user) async for user in users]

    return users
