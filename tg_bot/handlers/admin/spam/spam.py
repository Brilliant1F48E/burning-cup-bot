from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.admin import Spam

async def spam(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(" ")

    await call.message.answer("Введите текст сообщения:")
    await state.set_state(Spam.ENTER_TEXT)


async def enter_text(msg: types.Message, state=FSMContext):
    message_text = msg.text

    bot = msg.bot

    db_model = bot.get("db_model")

    users = await db_model.get_users()

    print(message_text)

    await state.finish()

    for user in users:
        try:
            await bot.send_message(
                chat_id=user.id,
                text=message_text
            )
        except Exception as ex:
            pass

    await msg.answer("Рассылка завершина")


def register_handlers_spam(dp: Dispatcher):
    dp.register_callback_query_handler(spam, text=["spam"], state="*", is_admin=True)
    dp.register_message_handler(enter_text, state=Spam.ENTER_TEXT, is_admin=True)
