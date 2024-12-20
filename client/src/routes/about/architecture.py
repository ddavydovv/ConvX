import os
from aiogram import Router
from aiogram.types import InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder


about_router = Router()


@about_router.callback_query(lambda query: query.data.startswith('О боте'))
async def FUNC_my_applications(query: CallbackQuery):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='Главная'))
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'Architecture_.png'), 'rb'),
            caption=f'''Архитектура данного бота является распределённой, 
что позволяет увеличить производительные мощности и отказоустойчивость, 
а также расширяет возможности горизонтального масштабирования.

Стек клиентской части: <b><i>Aiogram 3.12</i></b>, <b><i>AioHttp</i></b>, <b><i>Redis</i></b>, <b><i>RabbitMQ</i></b>

Стек серверных составляющих: <b><i>PostgreSQL</i></b>, <b><i>Redis</i></b>, <b><i>SqlAlchemy 2</i></b>, <b><i>RabbitMQ</i></b>, <b><i>FastAPI</i></b>, <b><i>Celery</i></b>, <b><i>S3</i></b>'''
        ),
        reply_markup=keyboard.as_markup()
    )


