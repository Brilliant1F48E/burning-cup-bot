from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback, notify_user
from tg_bot.models.db_model.models import Player, Member, Team

from tg_bot.types.team import TeamStatus
from tg_bot.types.player import PlayerStatus
from tg_bot.types.team_player import TeamPlayerStatus
from tg_bot.types.member import MemberStatus


async def unban_team(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    props = await parse_callback("unbanned_team", call.data)
    team_id = props.get("team_id")
    db_model = call.bot.get("db_model")

    team: Team = await db_model.get_team(team_id=team_id)

    team_players: list = await db_model.get_team_players_by_team_id(team_id=team.id)

    for team_player in team_players:
        player: Player = await db_model.get_player(player_id=team_player.player_id)
        member: Member = await db_model.get_member(member_id=player.member_id)

        await db_model.set_player_status(player_id=player.id, status=PlayerStatus.ACTIVE)
        await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.ACTIVE)
        await db_model.set_member_status(member_id=member.id, status=MemberStatus.ACTIVE)
        text_response: str = "<b>Разбан</b>\n\n" \
                      "Вы были навсегда разбаннены😊.\n" \
                      "По причине:\n" \
                      "Ещё раз извиняюсь, жду вас на турнире🔥"
        await notify_user(text_response,
                          chat_id=member.user_id,
                          bot=call.bot)

    await db_model.set_team_status(team_id=team_id, status=TeamStatus.ACTIVE)


def register_handlers_unban(dp: Dispatcher):
    dp.register_callback_query_handler(unban_team, text_contains=["unbanned_team"], state="*", is_admin=True)
