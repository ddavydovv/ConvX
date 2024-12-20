from aiogram import Router
from aiogram.types import CallbackQuery


hide_router = Router()


@hide_router.callback_query(lambda query: query.data.startswith('Скрыть'))
async def FUNC_hide(query: CallbackQuery) -> None:
    await query.message.delete()