from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.models.db_model.models import Team

# {
#     "id": "id",
#     "date": "date",
#     "status": "status",
#     "type": "type",
#     "item": {
#
#     }
# }


async def get_all(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    request_kb = bot.get("kb").get("request").get("team")
    db_model = bot.get("db_model")

    team_requests: list = await db_model.get_team_requests()

    requests: list = []

    for team_request in team_requests:
        team: Team = await db_model.get_team(team_id=team_request.team_id)
        requests.append({
            "id": team_request.id,
            "date": team_request.date_request,
            "status": team_request.request_status,
            "type": "team",
            "item": {
                "team_name": team.name
            }
        })
    ikb_view_all_requests: types.InlineKeyboardMarkup = await request_kb.get_all(requests=requests)

    answer_text = "<b>Запросы</b>\n\n" + "Выберите запрос:"

    await call.message.answer(text=answer_text, reply_markup=ikb_view_all_requests)


async def get_by_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("request")
    db_model = bot.get("db_model")


async def get_by_status_choice_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()


def register_handlers_get(dp: Dispatcher):
    dp.register_callback_query_handler(get_all, text_contains=["get_all"], is_admin=True)
