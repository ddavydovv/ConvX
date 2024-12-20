import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from servers.database.src.applications.service import applicationsDbRequests
from servers.database.src.config import settings
from servers.database.src.database.alchemy.utils import delete_database, create_database
from servers.database.src.users.router import users_router
from servers.database.src.applications.router import applications_router
from servers.database.src.utils.ampq.consumer import RabbitMQConsumer


@asynccontextmanager
async def lifespan(server: FastAPI):
    await delete_database()
    await create_database()
    server.include_router(users_router)
    server.include_router(applications_router)
    consume_task1 = asyncio.create_task(
        RabbitMQConsumer.consume(
            exchange_name='processing_documents',
            exchange_type='fanout',
            queue_name='processing_documents_database_queue',
            routing_key='',
            prefetch_count=1,
            callback_func=applicationsDbRequests.SQL_insert_application
        )
    )
    consume_task2 = asyncio.create_task(
        RabbitMQConsumer.consume(
            exchange_name='processing_documents_finished',
            exchange_type='direct',
            queue_name='processing_documents_finished_queue',
            routing_key='processing_documents_finished_key',
            prefetch_count=1,
            callback_func=applicationsDbRequests.SQL_application_processed
        )
    )
    yield
    consume_task1.cancel()
    consume_task2.cancel()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=settings.server.host,
        port=int(settings.server.port),
        reload=True
    )