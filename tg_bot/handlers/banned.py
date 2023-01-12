from aiogram import Dispatcher, types

from tg_bot.misc.phares import Phrases


async def banned_call(call: types.CallbackQuery):
    await call.answer(" ")

    message_text = Phrases.player_banned
    await call.message.answer(message_text)


async def banned_msg(msg: types.Message):
    message_text = Phrases.player_banned
    await msg.answer(message_text)


def register_handlers_banned(dp: Dispatcher):
    dp.register_callback_query_handler(banned_call, is_banned=True)
    dp.register_message_handler(banned_msg, is_banned=True)
