import os

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from client.src.utils.http import fetch_url


application_details_router = Router()


@application_details_router.callback_query(lambda query: query.data.startswith('Детали_'))
async def FUNC_application_details(query: CallbackQuery, state: FSMContext) -> None:
    message_id = query.data.split('_')[1]
    await state.update_data(details_application_id=message_id)
    url = 'http://127.0.0.1:8000/get-application-details'
    payload = {
        'message_id': message_id
    }
    headers = {
        'Content-Type': 'application/json'
    }
    URL_response = await fetch_url(url, payload, headers)
    data = URL_response['data']
    print(f'data: {data}')
    keyboard = InlineKeyboardBuilder()
    number = data['message_id']
    stock_format = data['mode'].split('_')[0]
    convert_format = data['mode'].split('_')[1]
    stock_file = data['filename']
    status = data['status']
    create_date = data['create_date']
    await state.update_data(stock_file=stock_file)
    if data['processed_date'] is not None:
        processed_date = data['processed_date']
        format_file = data['processed_filename']
        await state.update_data(format_file=format_file)
        keyboard.row(InlineKeyboardButton(text='Скачать обработанный', callback_data=f'СкачатьОб__{data['processed_filepath']}'))
    else:
        processed_date = '__-__-____'
        format_file = f'{data['filename'].split('.')[0]}.{data['mode'].split('_')[1].lower()}'
    keyboard.row(InlineKeyboardButton(text='Скачать исходник', callback_data=f'СкачатьИсх__{data['filepath']}'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='Заявки'))
    keyboard.row(InlineKeyboardButton(text='На главную', callback_data='Главная'))
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'applications_details.png'), 'rb'),
            caption=f'''Заявка <b><i>№{number}</i></b>:
            
<b><i>{stock_format}</i></b> ---> <b><i>{convert_format}</i></b>
<b><i>{stock_file}</i></b> ---> <b><i>{format_file}</i></b>
Статус заявки: <b><i>{status}</i></b>
Заявка создана: <b><i>{create_date}</i></b>
Заявка обработана: <b><i>{processed_date}</i></b>
'''
        ),
        reply_markup=keyboard.as_markup()
    )