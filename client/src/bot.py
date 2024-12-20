import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, Redis

from client.src.config import settings
from client.src.routes.about.architecture import about_router
from client.src.routes.applications.application_details import application_details_router
from client.src.routes.applications.application_download_file import download_stock_router
from client.src.routes.applications.applications import applications_router
from client.src.routes.start import start_router
from client.src.routes.convert.success import success_router
from client.src.routes.convert.waiting import waiting_router
from client.src.routes.convert.mode import mode_router
from client.src.routes.services_routes.hide import hide_router
from client.src.utils.ampq.consumer import RabbitMQConsumer
from client.src.services.notify_users import MessageHandler


async def main():
    bot = Bot(
        token=settings.bot.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    redis = Redis(host=settings.cache.url)
    dp = Dispatcher(
        storage=RedisStorage(redis=redis)
    )
    dp.include_router(start_router)
    dp.include_router(mode_router)
    dp.include_router(waiting_router)
    dp.include_router(success_router)
    dp.include_router(hide_router)
    dp.include_router(applications_router)
    dp.include_router(application_details_router)
    dp.include_router(download_stock_router)
    dp.include_router(about_router)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await asyncio.gather(
            dp.start_polling(bot),
            RabbitMQConsumer.consume(
                exchange_name='notify_users',
                exchange_type='direct',
                queue_name='notify_users_queue',
                routing_key='notify_users_key',
                prefetch_count=1,
                callback_func=MessageHandler.processing_file_finished_notify_users,
                bot=bot
            ),
            RabbitMQConsumer.consume(
                exchange_name='download_application',
                exchange_type='direct',
                queue_name='download_application_queue',
                routing_key='download_application_key',
                prefetch_count=1,
                callback_func=MessageHandler.downloading_file_finished_notify_users,
                bot=bot
            ),
        )
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    asyncio.run(main())