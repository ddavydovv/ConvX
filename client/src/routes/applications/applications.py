import os

from aiogram import Router
from aiogram.types import InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from client.src.utils.http import fetch_url


applications_router = Router()


@applications_router.callback_query(lambda query: query.data.startswith('Заявки'))
async def FUNC_my_applications(query: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    url = 'http://127.0.0.1:8000/get-applications'
    payload = {
        'user_id': query.from_user.id,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    URL_response = await fetch_url(url, payload, headers)
    SQL_data = URL_response['data']['applications_data']
    buttons = [
        InlineKeyboardButton(
            text=f'{application['filename'][:13]} | {application['status']}',
            callback_data=f'Детали_{application['message_id']}')
        for application in SQL_data['processing_applications']
    ]
    keyboard.add(*buttons)
    keyboard.adjust(1)
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='Главная'))
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'applications.png'), 'rb'),
            caption=f'''Пользователь: <b><i>{query.from_user.id}</i></b>
        
Всего обработано: <b><i>{SQL_data['processing_files_count']}</i></b>
Из них CSV файлов: <b><i>{SQL_data['processing_csv_count']}</i></b>
Из них XLSX файлов: <b><i>{SQL_data['processing_xlsx_count']}</i></b>
Из них PDF файлов: <b><i>{SQL_data['processing_pdf_count']}</i></b>
Из них TXT файлов: <b><i>{SQL_data['processing_txt_count']}</i></b>
Из них DOCX файлов: <b><i>{SQL_data['processing_docx_count']}</i></b>
'''
        ),
        reply_markup=keyboard.as_markup()
    )


