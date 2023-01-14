from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")

    requests_ikb = await admin_kb.get_team_requests_ikb()

    answer_text = "<b>Запросы</b>\n\n" + "Выбрать действие:"

    await call.message.answer(answer_text, reply_markup=requests_ikb)


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(menu, text=["request_team"], state="*", is_admin=True)

