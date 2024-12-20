from aiogram.types import InlineKeyboardButton, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from client.src.utils.s3.client import s3_client


class MessageHandler:

    @staticmethod
    async def processing_file_finished_notify_users(data, bot):
        user_id = data['user_id']
        processed_filename = data['processed_filename']
        processed_filepath = data['processed_filepath']
        message = data['event_message']
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text='Скрыть', callback_data='Скрыть'))
        file_stream = await s3_client.download_file(processed_filepath)
        file_stream.seek(0)
        await bot.send_document(
            chat_id=user_id,
            document=BufferedInputFile(
                file_stream.read(),
                filename=processed_filename
            ),
            caption=message,
            reply_markup=keyboard.as_markup()
        )

    @staticmethod
    async def downloading_file_finished_notify_users(data, bot):
        user_id = data['user_id']
        filepath = data['filepath']
        filename = data['filename']
        message = data['event_message']
        keyboard = InlineKeyboardBuilder()
        keyboard.row(InlineKeyboardButton(text='Скрыть', callback_data='Скрыть'))
        file_stream = await s3_client.download_file(filepath)
        file_stream.seek(0)
        await bot.send_document(chat_id=user_id,
            document=BufferedInputFile(
                file_stream.read(),
                filename=filename
            ), caption=message,
            reply_markup=keyboard.as_markup())