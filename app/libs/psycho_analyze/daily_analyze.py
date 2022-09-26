from pydantic import UUID4
from datetime import datetime, timedelta

from app.libs.postres_crud.queries import get_user_all_emotion_messages


async def get_recommendation(user_id: UUID4, from_date: datetime.now() - timedelta(days=1), to_date: datetime.now()):
    user_messages = await get_user_all_emotion_messages(user_id=user_id, from_at=from_date, to_at=to_date)
    emotion_counts = {}

    for message in user_messages:
        if emotion_counts.get(message['emotion'], None):
            emotion_counts[message['emotion']] += 1
        else:
            emotion_counts[message['emotion']] = 1

    if emotion_counts:
        max_emotion = max(emotion_counts, key=emotion_counts.get)
        max_emotion_count = emotion_counts[max_emotion]

        if max_emotion_count < 10:
            return None
    else:
        return None

    return max_emotion


async def get_text_recomandation():
    ...