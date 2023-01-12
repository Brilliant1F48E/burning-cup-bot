from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.registration import RegistrationStatus


async def set_registration(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

