from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards.request.request_kb import RequestKb
from tg_bot.misc.scripts import parse_callback


async def menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot: Bot = call.bot
    props: dict = await parse_callback("requests", call.data)
    requests_type = props.get("type")

    request_kb: RequestKb = bot.get("kb").get("request").get(requests_type)

    requests_ikb = await request_kb.get_menu()

    answer_text = "<b>Запросы</b>\n\n" + "Выбрать действие:"

    await call.message.answer(answer_text, reply_markup=requests_ikb)


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(menu, text_contains=["requests"], state="*", is_admin=True)

