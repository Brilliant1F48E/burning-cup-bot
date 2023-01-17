from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    request_kb = bot.get("kb").get("request").get("team")

    requests_ikb = await request_kb.get_menu(request_type="team")

    answer_text = "<b>Запросы</b>\n\n" + "Выбрать действие:"

    await call.message.answer(answer_text, reply_markup=requests_ikb)


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(menu, text=["request_team"], state="*", is_admin=True)

