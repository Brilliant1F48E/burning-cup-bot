from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.models.db_model.models import Team, RequestMember
from tg_bot.types.request import RequestStatus


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

    bot: Bot = call.bot
    props: dict = await parse_callback("get_all", call.data)

    requests_type: str = props.get("type")
    print(requests_type)
    request_kb = bot.get("kb").get("request").get(requests_type)
    db_model = bot.get("db_model")

    requests: list = await db_model.get_team_requests() if requests_type == "team" else await db_model.get_requests_member_by_status(status=RequestStatus.WAIT)

    requests_data: list = []

    for request in requests:
        data: dict = {
            "id": request.id,
            "date": request.date_request,
            "status": request.request_status if requests_type == "team" else request.request_member_status,
        }
        if requests_type == "team":
            team: Team = await db_model.get_team(team_id=request.team_id)
            data["item"] = {
                "team_name": team.name
            }
        elif requests_type == "member":
            request_member: RequestMember = await db_model.get_request_member(request_id=request.id)
            data["item"] = {
                "fullname": request_member.last_name + request_member.first_name + request_member.patronymic
            }
        requests_data.append(data)

    ikb_view_all_requests: types.InlineKeyboardMarkup = await request_kb.get_all(requests=requests_data)

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
