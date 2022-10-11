from platform_services.rabbitmq import RabbitMQWrapper
from aio_pika import Message, DeliveryMode
from app.schemas.adivce import AdviceResponce, AdvicePayload, Advice, AdviceBody, AdviceData
from app.schemas.messages import MessageWithEmotions, MessageWithAdvice, AdvicePayloadNew
from typing import List
import asyncio


rmq = RabbitMQWrapper()


async def mailer_advice(messages_with_advices: List[AdvicePayloadNew]):
    """ф-ция отвечает за рассылку личных советов пользователям"""
    for message in messages_with_advices:
        asyncio.create_task(push_processed_asset(message))    


async def push_processed_asset(payload: AdvicePayloadNew) -> None:
    """Отправляем структуру в sse"""
    #Переводим в итоговую схему респонса
    frame_message = AdviceResponce(
        payload=payload
    )
    body = frame_message.json().encode()
    channel = await rmq._get_channel()
    await channel.default_exchange.publish(
        Message(
            body=body,
            delivery_mode=DeliveryMode.PERSISTENT
        ), 
        routing_key=str(payload.user_id)
    )
    # print(f"Processed asset published {payload}")