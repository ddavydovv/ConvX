import io
import os
from datetime import datetime
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, Message, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from client.src.routes.convert.waiting import STATES_content
from client.src.utils.ampq.publisher import RabbitMQPublisher
from client.src.utils.s3.client import s3_client


success_router = Router()


@success_router.message(StateFilter(STATES_content.STATE_content_download))
async def FUNC_start_command(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    FSM_editable_message_id = data.get('FSM_editable_message_id')
    FSM_category = data.get('FSM_category')
    FSM_mode = data.get('FSM_mode')
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    if message.content_type == ContentType.DOCUMENT:
        if message.document.file_name.split('.')[1] == FSM_category.lower():
            if message.document.file_size <= 3 * 1024 * 1024:
                MESSAGE_user_id = message.from_user.id
                MESSAGE_message_id = message.message_id
                document = message.document
                file_id = document.file_id
                file_path = await message.bot.get_file(file_id)
                downloaded_file = await message.bot.download_file(file_path.file_path)
                filename = f'{document.file_name}'
                s3_path = f'{MESSAGE_user_id}/{FSM_category}/{FSM_mode}/{MESSAGE_message_id}.{document.file_name.split('.')[1]}'
                file_stream = io.BytesIO(downloaded_file.getvalue())
                file_stream.seek(0)
                await s3_client.upload_file(s3_path, file_stream)
                VAR_caption = 'Загрузка успешно завершена'
                body = {
                    'message_id': MESSAGE_message_id,
                    'user_id': MESSAGE_user_id,
                    'category': FSM_category,
                    'mode': FSM_mode,
                    'filename': filename,
                    'filepath': str(s3_path),
                    'create_date': str(datetime.now())
                }
                await RabbitMQPublisher.publish(
                    exchange_name='processing_documents',
                    exchange_type='fanout',
                    routing_key='',
                    body=body,
                )
                media = FSInputFile(os.path.join(media_dir, 'success.png'), 'rb')
            else:
                VAR_caption = f'Произошла ошибка. Отправьте документ размерностью <b><i>до 3 МБ</i></b>'
                media = FSInputFile(os.path.join(media_dir, 'success.png'), 'rb')
                await state.set_state(STATES_content.STATE_content_download)
        else:
            VAR_caption = f'Произошла ошибка. Отправьте документ в формате <b><i>{FSM_category}</i></b>'
            media = FSInputFile(os.path.join(media_dir, 'success.png'), 'rb')
            await state.set_state(STATES_content.STATE_content_download)
    else:
        VAR_caption = f'Произошла ошибка. Отправьте документ в формате <b><i>{FSM_category}</i></b>'
        media = FSInputFile(os.path.join(media_dir, 'success.png'), 'rb')
        await state.set_state(STATES_content.STATE_content_download)
    await message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='На главную', callback_data='Главная'))
    await message.bot.edit_message_media(
        chat_id=message.chat.id,
        message_id=FSM_editable_message_id,
        media=InputMediaPhoto(
            media=media,
            caption=VAR_caption
        ),
        reply_markup=keyboard.as_markup()
    )