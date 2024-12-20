import asyncio
import logging

from servers.processing.src.utils.logs.logger import logger
from servers.processing.src.utils.ampq.consumer import RabbitMQConsumer


async def main():
    try:
        await RabbitMQConsumer.consume(
            exchange_name='processing_documents',
            exchange_type='fanout',
            queue_name='processing_documents_processing_queue',
            routing_key='',
            prefetch_count=1,
        ),
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    asyncio.run(main())