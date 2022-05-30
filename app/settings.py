from functools import lru_cache
from logging import getLogger

from platform_services.wrapper_base import ServiceSettingsBase

logger = getLogger("settings")


class MongoCollectionsSubSettings(ServiceSettingsBase):
    ...


class RabbitMQEntitiesSubSettings(ServiceSettingsBase):
    ...


class Settings(ServiceSettingsBase):
    mongodb_database: str = "core-emotion"
    collections: MongoCollectionsSubSettings = MongoCollectionsSubSettings()
    rmq: RabbitMQEntitiesSubSettings = RabbitMQEntitiesSubSettings()
    ...


@lru_cache()
def get_settings() -> Settings:
    logger.info("Settings created")
    settings = Settings()
    return settings
