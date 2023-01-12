from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def cmd_start(msg: types.Message, state=FSMContext):
    await state.finish()

    answer_text = "Добро пожаловать администратор\n\nОжидайте анкеты"

    await msg.answer(text=answer_text)


def register_handler_menu(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state="*", is_moderator=True)
