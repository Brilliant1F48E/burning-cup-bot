from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def search_all(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")
    db_model = bot.get("db_model")

    team_requests = await db_model.get_team_requests()

    view_all_requests_ikb = await admin_kb.get_view_all_team_requests_ikb(team_requests=team_requests)

    answer_text = "<b>Запросы</b>\n\n" + "Выберите запрос:"

    await call.message.answer(text=answer_text, reply_markup=view_all_requests_ikb)


async def search_by_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")
    db_model = bot.get("db_model")

    search_by_status


async def search_by_status_choice_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()


def register_handlers_search(dp: Dispatcher):
    pass
