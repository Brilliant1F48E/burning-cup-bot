from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases
from tg_bot.misc.scripts import check_rule_team_player, parse_callback
from tg_bot.types.request import RequestStatus
from tg_bot.types.team import TeamStatus
from tg_bot.types.team_player import TeamPlayerStatus


async def disband_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    team_kb = call.bot.get('kb').get('team')
    db_model = call.bot.get("db_model")

    if not await check_rule_team_player(call=call):
        return

    team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
    team_id = team_player.team_id

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            answer_text = Phrases.captain_verification_block
            await call.message.answer(answer_text)
            return

    confirm_disband_team_ikb = await team_kb.get_confirm_disband_team(team_id=team_id)

    caption = Phrases.confirm_disband_team

    await call.bot.edit_message_caption(caption=caption,
                                        message_id=call.message.message_id,
                                        chat_id=call.message.chat.id,
                                        reply_markup=confirm_disband_team_ikb)


async def confirm_disband_team(call: types.CallbackQuery):
    await call.answer(' ')
    await call.message.delete()

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    props = await parse_callback('confirm_disband_team', call.data)

    team_id = props.get('team_id')

    captain_team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
    await db_model.set_team_player_is_ready(team_player_id=captain_team_player.id, is_ready=False)

    team_players = await db_model.get_team_players(team_id=team_id)

    for team_player in team_players:
        await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.DISBANDED)
        await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=False)
        await db_model.set_is_captain(team_player_id=team_player.id, is_captain=False)

    await db_model.set_team_status(team_id=team_id, status=TeamStatus.DISBANDED)

    answer_text = Phrases.success_disband_team

    await call.message.answer(text=answer_text, reply_markup=None)


def register_handlers_disband(dp: Dispatcher):
    dp.register_callback_query_handler(disband_team, text=["disband_team"], state='*', is_captain=True)

    dp.register_callback_query_handler(confirm_disband_team, text_contains=['confirm_disband_team'],
                                       is_captain=True)
