from sqlalchemy import select

from servers.database.src.database.alchemy.core import async_session
from servers.database.src.database.alchemy.models import USERS
from servers.database.src.users.schemas import AddUser, GetApplications


class usersDbRequests:

    @classmethod
    async def SQL_insert_user(cls, body: AddUser):
        async with async_session() as session:
            query = await session.execute(select(USERS).filter_by(user_id=str(body['user_id'])))
            user_scalar = query.scalar()

            if user_scalar is None:
                user = USERS(user_id=str(body['user_id']))
                session.add(user)
            else:
                pass
            await session.commit()

        return {
            'data': body
        }

    @classmethod
    async def SQL_get_user_details(cls, body: GetApplications):
        async with async_session() as session:

            response = {}

            query = await session.execute(select(USERS).filter_by(user_id=body['user_id']))
            query_data = query.scalar()

            response['user_id'] = query_data.user_id
            response['language'] = query_data.language
            response['role'] = query_data.role
            response['create_date'] = query_data.create_date.strftime('%Y-%m-%d %H:%M:%S')
            response['processing_files_count'] = query_data.processing_files_count
            response['processing_csv_count'] = query_data.processing_csv_count
            response['processing_xlsx_count'] = query_data.processing_xlsx_count
            response['processing_pdf_count'] = query_data.processing_pdf_count
            response['processing_txt_count'] = query_data.processing_txt_count
            response['processing_docx_count'] = query_data.processing_docx_count

        return {
            'data': response
        }