from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def add_match(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


def register_handlers_add_match(dp: Dispatcher):
    pass
