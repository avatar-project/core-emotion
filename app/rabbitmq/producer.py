from platform_services.rabbitmq import RabbitMQWrapper
from aio_pika import Message, DeliveryMode
from app.schemas.adivce import AdviceResponce, AdvicePayload, Advice, AdviceBody, AdviceData
from app.schemas.messages import MessageWithEmotions, MessageWithAdvice, AdvicePayloadNew, AdviceResponceNew
from typing import List
import asyncio
import logging

rmq = RabbitMQWrapper()
logger = logging.getLogger("rmq.user")


async def mailer_advice(messages_with_advices: List[AdvicePayloadNew]):
    """ф-ция отвечает за рассылку личных советов пользователям"""
    for message in messages_with_advices:
        asyncio.create_task(push_processed_asset(message))    


async def push_processed_asset(payload: AdvicePayloadNew) -> None:
    """Отправляем структуру в sse"""
    #Переводим в итоговую схему респонса
    frame_message = AdviceResponceNew(
        payload=payload
    )
    body = frame_message.json().encode()
    print("Magick")
    try:
        channel = await rmq._get_channel()
        user = await channel.get_queue(str(payload.user_id))
        print("Magick 2")
        await channel.default_exchange.publish(
            Message(
                body=body,
                delivery_mode=DeliveryMode.PERSISTENT
            ), 
            routing_key=str(payload.user_id)
        )
        logger.info(f'Send to sse {payload.user_id} user')
    except Exception as e:
        logger.info(f'User {payload.user_id} offline')
