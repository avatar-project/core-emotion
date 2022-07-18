from functools import lru_cache
from logging import getLogger

from platform_services.wrapper_base import ServiceSettingsBase

logger = getLogger("settings")


class MongoCollectionsSubSettings(ServiceSettingsBase):
    users: str = "users"
    message: str = "message"


class RabbitMQEntitiesSubSettings(ServiceSettingsBase):
    ...


class Settings(ServiceSettingsBase):
    users_mongodb_database: str = "user_api"
    communication_system_mongodb_database: str = "communication_system"
    # mongodb_database: str = "core-emotion"
    collections: MongoCollectionsSubSettings = MongoCollectionsSubSettings()
    rmq: RabbitMQEntitiesSubSettings = RabbitMQEntitiesSubSettings()
    ...


@lru_cache()
def get_settings() -> Settings:
    logger.info("Settings created")
    settings = Settings()
    return settings
