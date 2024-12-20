import json
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from servers.database.src.applications.schemas import AddApplication, GetApplications
from servers.database.src.cache.redis.core import redis_client
from servers.database.src.database.alchemy.core import async_session
from servers.database.src.database.alchemy.models import APPLICATIONS, USERS
from servers.database.src.utils.ampq.publisher import RabbitMQPublisher


class applicationsDbRequests:

    @classmethod
    async def SQL_insert_application(cls, body: AddApplication):
        async with async_session() as session:
            query = await session.execute(
                select(APPLICATIONS).filter_by(
                    message_id=str(body['message_id'])
                )
            )
            application_scalar = query.scalar()

            if application_scalar is None:

                status = 'В обработке'

                body['status'] = status

                application = APPLICATIONS(
                    message_id=str(body['message_id']),
                    user_id=str(body['user_id']),
                    category=body['category'],
                    mode=body['mode'],
                    filename=body['filename'],
                    filepath=str(body['filepath']),
                    processed_filename=None,
                    processed_filepath=None,
                    status=status,
                    create_date=str(body['create_date']),
                    processed_date=None
                )
                session.add(application)
                await session.flush()
                await session.commit()
            else:
                pass

        return {
            'data': body
        }

    @classmethod
    async def SQL_application_processed(cls, body: AddApplication):
        async with async_session() as session:

            user_id: str = body['user_id']
            message_id: str = body['message_id']

            get_applications_key = f'get_applications: {user_id}'
            get_application_details_key = f'get_application_details: {message_id}'

            if await redis_client.exists(get_applications_key):
                await redis_client.delete(get_applications_key)
            if await redis_client.exists(get_application_details_key):
                await redis_client.delete(get_application_details_key)

            query = await session.execute(
                select(APPLICATIONS).filter_by(
                    message_id=str(body['message_id'])
                )
            )
            application_scalar = query.scalar()

            status = 'Обработано'
            processed_date = str(datetime.now())

            if application_scalar is not None:
                application_scalar.status = status
                application_scalar.processed_date = processed_date
                application_scalar.processed_filename = str(body['processed_filename'])
                application_scalar.processed_filepath = str(body['processed_filepath'])
            else:
                application = APPLICATIONS(
                    message_id=str(body['message_id']),
                    user_id=str(body['user_id']),
                    category=body['category'],
                    mode=body['mode'],
                    filename=body['filename'],
                    filepath=str(body['filepath']),
                    processed_filename=body['processed_filename'],
                    processed_filepath=str(body['processed_filepath']),
                    status=status,
                    create_date=str(body['create_date']),
                    processed_date=str(datetime.now())
                )
                session.add(application)

            body['status'] = status
            body['processed_date'] = processed_date
            body['event_message'] = 'Ваша заявка была успешно выполнена'

            await session.flush()
            await session.commit()

            await RabbitMQPublisher.publish(
                exchange_name='notify_users',
                exchange_type='direct',
                routing_key='notify_users_key',
                body=body
            )

        return {
            'data': body
        }

    @classmethod
    async def SQL_get_applications(cls, body: GetApplications):
        async with async_session() as session:

            user_id: str = body['user_id']

            cache_key = f'get_applications: {user_id}'
            cached_data = await redis_client.get(cache_key)

            if cached_data:
                response = json.loads(cached_data)
            else:
                query = await session.execute(
                    select(USERS).filter_by(
                        user_id=str(user_id)
                    ).options(
                        selectinload(USERS.user_applications)
                    )
                )
                query_data = query.scalar()

                response = {
                    'user_id': query_data.user_id,
                    'processing_files_count': query_data.processing_files_count,
                    'processing_csv_count': query_data.processing_csv_count,
                    'processing_xlsx_count': query_data.processing_xlsx_count,
                    'processing_pdf_count': query_data.processing_pdf_count,
                    'processing_txt_count': query_data.processing_txt_count,
                    'processing_docx_count': query_data.processing_docx_count,
                    'processing_applications': [
                        {
                            'message_id': application.message_id,
                            'filename': application.filename,
                            'processed_filename': application.processed_filename,
                            'status': application.status
                        } for application in query_data.user_applications
                    ]
                }

            return {
                'data': {
                    'applications_data': response
                }
            }

    @classmethod
    async def SQL_get_application_details(cls, body: GetApplications):
        async with async_session() as session:

            message_id: str = body['message_id']

            cache_key = f'get_application_details: {message_id}'
            cached_data = await redis_client.get(cache_key)

            if cached_data:
                response = json.loads(cached_data)
            else:
                response = {}

                query = await session.execute(
                    select(APPLICATIONS).filter_by(
                        message_id=body['message_id']
                    )
                )
                query_data = query.scalar()

                response['message_id'] = query_data.message_id
                response['user_id'] = query_data.user_id
                response['category'] = query_data.category
                response['mode'] = query_data.mode
                response['filename'] = query_data.filename
                response['filepath'] = query_data.filepath
                response['processed_filename'] = query_data.processed_filename
                response['processed_filepath'] = query_data.processed_filepath
                response['status'] = query_data.status
                response['create_date'] = query_data.create_date
                response['processed_date'] = query_data.processed_date

                await redis_client.set(
                    cache_key,
                    json.dumps(response),
                    ex=1000
                )

            return {
                'data': response
            }