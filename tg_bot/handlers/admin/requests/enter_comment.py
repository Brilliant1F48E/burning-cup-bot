from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import notify_user
from tg_bot.models.db_model.models import RequestTeam, TeamPlayer, Player, Member, RequestMember
from tg_bot.types.request import RequestStatus
from tg_bot.types.request.states import ModerationRequestEnterComment


async def enter_comment_team_request(msg: types.Message, state: FSMContext):
    await msg.delete()

    comment: str = msg.text
    db_model = msg.bot.get('db_model')
    state_data: dict = await state.get_data()
    request_id: str = state_data.get("request_id")

    await db_model.set_request_team_status(request_team_id=request_id, request_status=RequestStatus.FAIL)
    await db_model.set_request_team_comment(request_team_id=request_id, comment=comment)
    request_team: RequestTeam = await db_model.get_request_team(request_team_id=request_id)

    team_player_captain: TeamPlayer = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
    player: Player = await db_model.get_player(player_id=team_player_captain.player_id)
    member: Member = await db_model.get_member(member_id=player.member_id)

    message_text: str = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                        'По причине:\n' \
                        f'{request_team.comment}'

    await notify_user(
        chat_id=member.user_id,
        text=message_text,
        bot=msg.bot
    )

    answer_text: str = "<b>Команда успешно не допущена к участию.</b>\n" \
                       f"По причине:\n{comment}"

    await msg.answer(text=answer_text)

    await state.finish()


async def enter_comment_member_request(msg: types.Message, state: FSMContext):
    await msg.delete()

    comment: str = msg.text

    db_model = msg.bot.get('db_model')

    state_data: dict = await state.get_data()

    request_id: str = state_data.get("request_id")

    request_member: RequestMember = await db_model.get_request_member(request_id=request_id)
    await db_model.set_request_member_status(request_id=request_id, status=RequestStatus.FAIL)
    await db_model.set_request_member_comment(request_id=request_id, comment=comment)
    register_kb = msg.bot.get('kb').get('register')
    repeated_request_member_ikb = await register_kb.get_repeated_request_member_ikb()
    await notify_user(bot=msg.bot, text=f'<b>❌ Вы не прошли верификацию</b>\n\n'
                                        f'<b>По причине:</b>\n{comment}', chat_id=request_member.user_id,
                      reply_markup=repeated_request_member_ikb)

    answer_text: str = "<b>Участник успешно не верифицированн</b>\n" \
                       f"По причине:\n{comment}"

    await msg.answer(text=answer_text)

    await state.finish()


def register_handlers_enter_comment(dp: Dispatcher):
    dp.register_message_handler(enter_comment_team_request, state=ModerationRequestEnterComment.ENTER_COMMENT,
                                is_admin=True)
    dp.register_message_handler(enter_comment_member_request, state=ModerationRequestEnterComment.ENTER_COMMENT,
                                is_admin=True)
