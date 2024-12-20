import os
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto

from client.src.utils.http import fetch_url


start_router = Router()


@start_router.message(CommandStart())
async def FUNC_start_command(message: Message, state: FSMContext):
    MESSAGE_user_id = message.from_user.id
    await state.update_data(FSM_user_id=MESSAGE_user_id)
    url = 'http://127.0.0.1:8000/auth'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'user_id': str(MESSAGE_user_id)
    }
    await fetch_url(url, payload, headers)
    await message.delete()
    button1 = InlineKeyboardButton(text='.PDF', callback_data='Категория_PDF')
    # button2 = InlineKeyboardButton(text='.WORD', callback_data='Категория_WORD')
    # button3 = InlineKeyboardButton(text='.EXCEL', callback_data='Категория_EXCEL')
    # button4 = InlineKeyboardButton(text='.CSV', callback_data='Категория_CSV')
    # button5 = InlineKeyboardButton(text='.TXT', callback_data='Категория_TXT')
    button6 = InlineKeyboardButton(text='Мои заявки', callback_data='Заявки')
    button7 = InlineKeyboardButton(text='О боте', callback_data='О боте')
    KB = [
        [button1],
        [button6],
        [button7]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=KB)
    media_dir = os.path.join(os.path.dirname(__file__), '..', 'media')
    editable_message = await message.answer_photo(
        photo=FSInputFile(os.path.join(media_dir, 'main.png'), 'rb'),
        caption='Главное меню:',
        reply_markup=keyboard
    )
    await state.update_data(FSM_editable_message_id=editable_message.message_id)



@start_router.callback_query(lambda query: query.data.startswith('Главная'))
async def FUNC_start_command(query: CallbackQuery, state: FSMContext) -> None:
    MESSAGE_user_id = query.from_user.id
    await state.update_data(FSM_user_id=MESSAGE_user_id)
    button1 = InlineKeyboardButton(text='.PDF', callback_data='Категория_PDF')
    # button2 = InlineKeyboardButton(text='.WORD', callback_data='Категория_WORD')
    # button3 = InlineKeyboardButton(text='.EXCEL', callback_data='Категория_EXCEL')
    # button4 = InlineKeyboardButton(text='.CSV', callback_data='Категория_CSV')
    # button5 = InlineKeyboardButton(text='.TXT', callback_data='Категория_TXT')
    button6 = InlineKeyboardButton(text='Мои заявки', callback_data='Заявки')
    button7 = InlineKeyboardButton(text='О боте', callback_data='О боте')
    KB = [
        [button1],
        [button6],
        [button7]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=KB)
    media_dir = os.path.join(os.path.dirname(__file__), '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'main.png'), 'rb'),
            caption='Главное меню:'
        ),
        reply_markup=keyboard
    )