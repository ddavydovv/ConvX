import os
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder


waiting_router = Router()


class STATES_content(StatesGroup):
    STATE_content_download = State()


@waiting_router.callback_query(lambda query: query.data.startswith('Режим_'))
async def FUNC_start_command(query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    FSM_category = data.get('FSM_category')
    QUERY_mode = f'{FSM_category}_{query.data.split('_')[2]}'
    await state.update_data(FSM_mode=QUERY_mode)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data=f'Категория_{FSM_category}'))
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'waiting.png'), 'rb'),
            caption=f'Отправьте документ который вы хотите конвертировать из <b><i>{FSM_category}</i></b> в <b><i>{query.data.split('_')[2]}</i></b>'
        ),
        reply_markup=keyboard.as_markup()
    )
    await state.set_state(STATES_content.STATE_content_download)
