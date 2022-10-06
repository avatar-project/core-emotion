from platform_services.rabbitmq import RabbitMQWrapper
from aio_pika import Message, DeliveryMode
from app.schemas.adivce import AdviceResponce, AdvicePayload, Advice, AdviceBody, AdviceData
from app.schemas.messages import MessageWithEmotions, MessageWithAdvice
from typing import List
import asyncio


rmq = RabbitMQWrapper()


async def mailer_advice(messages_with_advices: List[MessageWithAdvice]):
    """ф-ция отвечает за рассылку личных советов пользователям"""
    print("new task", messages_with_advices)
    for message in messages_with_advices:
        print("new task")
        asyncio.create_task(push_processed_asset(message))    


async def push_processed_asset(payload: AdviceResponce) -> None:
    #Переводим в итоговую схему респонса
    # ("start")
    frame_message = AdviceResponce(
        payload=payload
    )
    body = frame_message.json().encode()
    async with rmq.channel_pool.acquire() as channel:
        await channel.default_exchange.publish(
            Message(
                body=body,
                delivery_mode=DeliveryMode.PERSISTENT
            ), 
            routing_key=str(payload.payload.user_id)
        )
    print(f"Processed asset published {payload}")