import os
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder


mode_router = Router()


@mode_router.callback_query(lambda query: query.data.startswith('Категория_'))
async def FUNC_start_command(query: CallbackQuery, state: FSMContext) -> None:
    QUERY_category = query.data.split('_')[1]
    await state.update_data(FSM_category=QUERY_category)
    keyboard = InlineKeyboardBuilder()
    if QUERY_category == 'PDF':
        keyboard.row(InlineKeyboardButton(text='.PDF > .WORD', callback_data='Режим_PDF_WORD'))
        # keyboard.row(InlineKeyboardButton(text='.PDF > .TXT', callback_data='Режим_PDF_TXT'))
    elif QUERY_category == 'WORD':
        keyboard.row(InlineKeyboardButton(text='.WORD > .PDF', callback_data='Режим_WORD_PDF'))
        keyboard.row(InlineKeyboardButton(text='.WORD > .TXT', callback_data='Режим_WORD_TXT'))
    elif QUERY_category == 'EXCEL':
        keyboard.row(InlineKeyboardButton(text='.EXCEL > .CSV', callback_data='Режим_EXCEL_CSV'))
    elif QUERY_category == 'CSV':
        keyboard.row(InlineKeyboardButton(text='.CSV > .EXCEL', callback_data='Режим_CSV_EXCEL'))
    else:
        keyboard.row(InlineKeyboardButton(text='.TXT > .WORD', callback_data='Режим_TXT_WORD'))
        keyboard.row(InlineKeyboardButton(text='.TXT > .PDF', callback_data='Режим_TXT_PDF'))
        keyboard.row(InlineKeyboardButton(text='.TXT > .CSV', callback_data='Режим_TXT_CSV'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='Главная'))
    media_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    await query.bot.edit_message_media(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(os.path.join(media_dir, 'mode.png'), 'rb'),
            caption='Выберите режим:'
        ),
        reply_markup=keyboard.as_markup()
    )