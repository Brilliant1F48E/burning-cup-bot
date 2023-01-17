from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases
from tg_bot.misc.scripts import check_rule_team_player, parse_callback, notify_user
from tg_bot.types.request import RequestStatus
from tg_bot.types.team_player import TeamPlayerStatus


async def kick_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    team_kb = call.bot.get('kb').get('team')
    db_model = call.bot.get('db_model')

    if not await check_rule_team_player(call=call):
        return

    current_team_player = await db_model.get_team_player_by_user_id(user_id=call.from_user.id)

    request_team = await db_model.get_request_team_by_team_id(team_id=current_team_player.team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            answer_text = Phrases.captain_verification_block
            await call.message.answer(answer_text)
            return

    props = await parse_callback(method='kick_team_player', callback_data=call.data)
    player_id = props.get('player_id')

    confirm_kick_team_player_ikb = await team_kb.get_confirm_kick_team_player_ikb(player_id=player_id)
    player = await db_model.get_player(player_id=player_id)

    answer_text = Phrases.confirm_kick_team_player + f' {player.username}?'

    await call.message.answer(answer_text, reply_markup=confirm_kick_team_player_ikb)


async def confirm_kick_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    props = await parse_callback(method='confirm_kick_team_player', callback_data=call.data)
    player_id = props.get('player_id')

    team_player = await db_model.get_team_player_by_player_id(player_id=player_id)

    await db_model.set_team_player_status_by_player_id(team_player_id=team_player.id, status=TeamPlayerStatus.KICK)
    await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=False)

    answer_text = Phrases.success_kick_team_player

    player = await db_model.get_player(player_id=player_id)
    member = await db_model.get_member(member_id=player.member_id)

    await notify_user(text=Phrases.kick_from_team, bot=call.bot, chat_id=member.user_id)
    await call.message.answer(answer_text)


def register_handlers_kick(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_kick_player, text_contains=['confirm_kick_team_player'], state='*',
                                       is_captain=True)
    dp.register_callback_query_handler(kick_player, text_contains=['kick_team_player'], state='*',
                                       is_captain=True)
