from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def choice_request_type(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(" ")


def register_handlers_choice_request_type(dp: Dispatcher):
    dp.register_callback_query_handler(choice_request_type, text=["choice_request_type"], state="*")
