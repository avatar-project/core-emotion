from app.settings import get_settings
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from platform_services.mongodb.injectors import mongodb_client

settings = get_settings()


def mongodb_user_database() -> AsyncIOMotorDatabase:
    return mongodb_client().get_database(settings.users_mongodb_database)


def mongodb_communicator_dabtabase() -> AsyncIOMotorDatabase:
    return mongodb_client().get_database(settings.communication_system_mongodb_database)


def messages_collection() -> AsyncIOMotorCollection:
    return mongodb_communicator_dabtabase()[settings.collections.message]


def users_collection() -> AsyncIOMotorCollection:
    return mongodb_user_database()[settings.collections.users]
