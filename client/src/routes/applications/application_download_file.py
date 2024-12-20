import os
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from client.src.utils.ampq.publisher import RabbitMQPublisher


download_stock_router = Router()


@download_stock_router.callback_query(lambda query: query.data.startswith('СкачатьИсх__') or query.data.startswith('СкачатьОб__'))
async def FUNC_start_command(query: CallbackQuery, state: FSMContext) -> None:
    print(query.data)
    data = await state.get_data()
    application_id = data.get('details_application_id')
    if query.data.startswith('СкачатьИсх__'):
        filename = data.get('stock_file')
    else:
        filename = data.get('format_file')
    body = {
        'user_id': query.from_user.id,
        'filepath': query.data.split('__')[1],
        'filename': filename,
        'event_message': 'Ваша заявка на скачивание файла выполнена!'
    }
    await RabbitMQPublisher.publish(
        exchange_name='download_application',
        exchange_type='direct',
        routing_key='download_application_key',
        body=body
    )
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data=f'Детали_{application_id}'))
    keyboard.row(InlineKeyboardButton(text='На главную', callback_data='Главная'))
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'downloading_application_added.png'), 'rb'),
            caption=f'Заявка на скачивание принята. Мы отправим вам файл как только он будет готов!'
        ),
        reply_markup=keyboard.as_markup()
    )