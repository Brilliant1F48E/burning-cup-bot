from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def rules(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    with open("Регламент.pdf", "rb") as document:
        await call.bot.send_document(
            chat_id=call.from_user.id,
            document=document
        )


def register_handlers_rules(dp: Dispatcher):
    dp.register_callback_query_handler(rules, text=["rules"], state="*")