import json
import aiormq

from servers.processing.src.config import settings


class RabbitMQPublisher:

    @classmethod
    async def publish(cls, exchange_name, exchange_type, routing_key, body):
        connection = await aiormq.connect(settings.rabbit.url)
        channel = await connection.channel()
        await channel.exchange_declare(
            exchange_name,
            exchange_type=exchange_type
        )
        await channel.basic_publish(
            body=json.dumps(body).encode('utf-8'),
            exchange=exchange_name,
            routing_key=routing_key
        )