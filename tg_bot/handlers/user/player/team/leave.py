from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases
from tg_bot.misc.scripts import check_rule_team_player
from tg_bot.models.db_model.models import TeamPlayer
from tg_bot.types.request import RequestStatus
from tg_bot.types.team_player import TeamPlayerStatus


async def leave_the_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(" ")

    team_kb = call.bot.get('kb').get('team')

    confirm_leave_the_team_ikb = await team_kb.get_confirm_leave_the_team_ikb()
    db_model = call.bot.get('db_model')

    team_player: TeamPlayer = await db_model.get_team_player(user_id=call.from_user.id)

    if not await check_rule_team_player(call=call):
        return

    if team_player:
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        if request_team:
            if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
                answer_text = Phrases.team_player_verification_block
                await call.message.answer(answer_text)
                return

    answer_text = Phrases.confirm_leave_from_team
    await call.message.answer(answer_text, reply_markup=confirm_leave_the_team_ikb)


async def confirm_leave_the_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(" ")

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    team_player: TeamPlayer = await db_model.get_team_player(user_id=user_id)

    await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.LEAVE)

    await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=False)

    answer_text = Phrases.success_leave_from_team
    await call.message.answer(answer_text)


def register_handlers_leave(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_leave_the_team, text_contains=['confirm_leave_from_team'], state='*',
                                       is_team_player=True)
    dp.register_callback_query_handler(leave_the_team, text_contains=['leave_from_team'], state='*',
                                       is_team_player=True)
