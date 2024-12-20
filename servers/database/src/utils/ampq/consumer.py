import asyncio
import json
from functools import partial
import aiormq
from aiormq.abc import DeliveredMessage

from servers.database.src.config import settings


class RabbitMQConsumer:

    @classmethod
    async def consume(cls, exchange_name, exchange_type, queue_name, routing_key, prefetch_count, callback_func):
        connection = await aiormq.connect(settings.rabbit.url)
        channel = await connection.channel()
        await channel.exchange_declare(
            exchange_name,
            exchange_type=exchange_type
        )
        declare_ok = await channel.queue_declare(queue_name)
        await channel.queue_bind(
            queue=declare_ok.queue,
            exchange=exchange_name,
            routing_key=routing_key
        )
        await channel.basic_qos(prefetch_count=prefetch_count)
        await channel.basic_consume(
            declare_ok.queue,
            partial(
                cls.on_message,
                callback_func
            ),
            no_ack=False
        )
        await asyncio.Future()

    @staticmethod
    async def on_message(callback, message: DeliveredMessage):
        body: list = json.loads(message.body.decode())
        await callback(body)
        await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag)
