from uuid import UUID
from pydantic import UUID4
from datetime import datetime, timedelta, timezone, date

from app.libs.postres_crud.queries import get_user_all_emotion_messages, get_user_state
from app.schemas.adivce import EmotionType


async def get_date_emotion_count(user_id: UUID4, from_date: datetime, to_date: datetime) -> dict:
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


async def recommender_variant(user_id: UUID4) -> int:
    to_at = date.today() + timedelta(days=1)
    from_at = to_at - timedelta(days=7)
    user_states = await get_user_state(user_id=user_id, from_at=from_at, to_at=to_at)

    cur_state = user_states[-1]['state']
    cur_state_count = 1
    for user_state in range(len(user_states)-2, 0, -1):
        if user_state['state'] != cur_state:
            break
        cur_state_count += 1

    return cur_state_count

    # if cur_state_count > 6:
    #     return 3
    # elif cur_state_count > 2:
    #     return 2
    # else:
    #     return 1


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
