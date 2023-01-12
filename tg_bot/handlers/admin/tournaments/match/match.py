from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def match(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_ikb = call.bot.get('kb').get('admin')

    match_ikb = await admin_ikb.get_match_ikb()

