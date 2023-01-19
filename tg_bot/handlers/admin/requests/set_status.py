from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from tg_bot.handlers.admin.requests.add_tournament_team import add_tournament_team
from tg_bot.handlers.admin.requests.close_registration import close_registration
from tg_bot.keyboards import RequestTeamKb
from tg_bot.misc.scripts import parse_callback
from tg_bot.models.db_model.models import RequestTeam, TeamPlayer, Tournament, Registration
from tg_bot.types.registration import RegistrationStatus
from tg_bot.types.request import RequestStatus


async def choice_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    props: dict = await parse_callback("choice_status", call.data)
    request_type: str = props.get("type")
    request_id: str = props.get("id")

    request_kb: RequestTeamKb = call.bot.get("kb").get("request").get(request_type)

    ikb_choice_status: types.InlineKeyboardMarkup = await request_kb.choice_status(request_id=request_id)

    answer_text: str = "<b>Запрос</b>\n\nВыберите статус:"

    await call.message.answer(
        text=answer_text,
        reply_markup=ikb_choice_status
    )


async def set_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()
    await call.answer(" ")
    await state.finish()

    bot: Bot = call.bot
    db_model = bot.get("db_model")

    props: dict = await parse_callback("set_status", call.data)
    request_type: str = props.get("type")
    request_id: str = props.get("id")
    request_status: str = props.get("status")

    print(request_id)
    tournament: Tournament = await db_model.get_tournament()
    registration: Registration = await db_model.get_registration(tournament_id=tournament.id)

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    if request_status == RequestStatus.SUCCESS:
        request_team: RequestTeam = await db_model.get_request_team(request_team_id=request_id)
        captain: TeamPlayer = await db_model.get_captain_by_team_id(team_id=request_team.team_id)

        await add_tournament_team(db_model=db_model, request_team=request_team, bot=bot, captain=captain)

        tournament_teams = await db_model.get_tournament_teams()
        if len(tournament_teams) == tournament.limit_teams:
            await close_registration(db_model=db_model, bot=bot, registration=registration)

    answer_text: str = "<b>Статус запроса успешно изменён</b>"

    await db_model.set_request_team_status(request_team_id=request_id, request_status=request_status)

    await call.message.answer(answer_text)


def register_handlers_set_status(dp: Dispatcher):
    dp.register_callback_query_handler(choice_status, text_contains=["choice_status"], state="*", is_admin=True)
    dp.register_callback_query_handler(set_status, text_contains=["set_status"], state="*", is_admin=True)
