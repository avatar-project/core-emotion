from uuid import UUID
from pydantic import UUID4
from datetime import datetime, timedelta, timezone, date

from app.libs.postres_crud.queries import get_user_all_emotion_messages
from app.schemas.adivce import EmotionType


async def get_date_emotion_count(user_id: UUID4, from_date: datetime, to_date: datetime):
    user_messages = await get_user_all_emotion_messages(user_id=user_id, from_at=from_date, to_at=to_date)
    emotion_counts = {
        'neutral': 0,
        'joy': 0,
        'anger': 0,
        'sadness': 0,
        'fear': 0,
        'surprise': 0
    }

    for message in user_messages:
        emotion_counts[message['emotion']] += 1

    return emotion_counts


async def _get_datetime_drom_date(udate):
    return datetime(udate.year, udate.month, udate.day, tzinfo=timezone.utc)


async def main_emotion(user_id: UUID4):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    today = await _get_datetime_drom_date(today)
    tomorrow = await _get_datetime_drom_date(tomorrow)

    emotion_counts = await get_date_emotion_count(user_id, today, tomorrow)

    emotion_counts.pop('neutral', None)
    emotion_counts.pop('surprise', None)

    if not _check_on_message_count(emotion_counts):
        return EmotionType.NEUTRAL

    max_emotion = max(emotion_counts, key=emotion_counts.get)

    return max_emotion


async def _check_on_message_count(self, emotion_counts: dict) -> bool:
    MIN_MESSAGE_COUNT = 5
    message_count = 0

    for k, v in emotion_counts.items():
        message_count += v

    if message_count < MIN_MESSAGE_COUNT:
        return False

    return True


async def get_daily_recomandation(user_id: UUID4, from_date: datetime, to_date: datetime):
    ...


async def get_text_recomandation():
    ...
