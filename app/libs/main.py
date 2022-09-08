from app.libs.psycho_analyze.analyze import calculate_coef, get_advice, get_text_sents, message_get_psycho_metrics, sents_get_psycho_metrics
from app.schemas.messages import MessageBase, MessageWithEmotions


async def psycho_text_analyze(message: MessageBase):
    """Основная функция, в которой сообщения проходит весь пайплайн от предобработки и вычесления метрик до записи в базу и отправки пользователю

    Args:
        message (MessageBase): сообщение 
    """
    sents = await get_text_sents(message.content)  # Разбиваем сообщение на предложения
    # Анализируем каждое предложение
    sents_emotion_list = await sents_get_psycho_metrics(sents)
    # Анализируем все предложение
    message_with_emotion = await message_get_psycho_metrics(message)
    # Находим итоговую эмоцию для сообщения
    # print(sents_emotion_list)
    # print(message_with_emotion)
    message_emotion = await calculate_coef(message_with_emotion, sents_emotion_list)
    advices = await get_advice(message, message_emotion)

    message_with_emotion = MessageWithEmotions(
        message_id=message.message_id,
        emotion=message_emotion,
        advice=advices
    )
    # await save_all_sents(message_with_emotion)

    return message_with_emotion
