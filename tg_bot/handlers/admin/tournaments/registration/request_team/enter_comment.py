from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import notify_user
from tg_bot.types.moderator import VerifRequestTeam
from tg_bot.types.request import RequestStatus


async def enter_comment_team_request(msg: types.Message, state: FSMContext):
    await msg.delete()

    comment = msg.text

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()

    request_team_id = state_data.get('request_team_id')

    await db_model.set_request_team_status(request_team_id=request_team_id, status=RequestStatus.FAIL)
    await db_model.set_request_team_comment(request_team_id=request_team_id, comment=comment)
    request_team = await db_model.get_request_team(request_team_id=request_team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
    player = await db_model.get_player(player_id=team_player_captain.player_id)
    member = await db_model.get_member(member_id=player.member_id)

    message_text = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                   'По причине:\n' \
                   f'{request_team.comment}'

    await notify_user(
        chat_id=member.user_id,
        text=message_text,
        bot=msg.bot
    )


def register_handlers_enter_comment(dp: Dispatcher):
    dp.register_message_handler(enter_comment_team_request, state=VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM, is_admin=True)
