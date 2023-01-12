from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback


async def view_request_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")

    bot = call.bot
    db_model = bot.get("db_model")
    admin_kb = bot.get("kb").get("admin")

    props = await parse_callback("view_request_team", call.data)

    team_id = props.get("team_id")

    team = await db_model.get_team(team_id=team_id)

    captain = await db_model.get_captain_by_team_id(team_id=team_id)

    team_players = await db_model.get_team_players_without_captain(team_id=team_id)


async def request_team_moderation(call: types.CallbackQuery):
    await call.answer(" ")
    pass


async def enter_comment_request_team(msg: types.Message, state=FSMContext):
    pass

    await state.finish()


def register_handlers_moderation(dp: Dispatcher):
    dp.register_callback_query_handler(view_request_team, text_contains=['view_request_team'], state='*',
                                       is_admin=True)
    dp.register_callback_query_handler(request_team_moderation, text_contains=['moderation_request_team'], state='*',
                                       is_admin=True)
    dp.register_message_handler(enter_comment_request_team, state=VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM,
                                is_admin=True)
