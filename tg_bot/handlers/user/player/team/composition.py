from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.request import RequestStatus


# TEAM PLAYER
async def team_composition(call: types.CallbackQuery, state: FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    team_kb = call.bot.get('kb').get('team')

    current_team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

    team_id = current_team_player.team_id

    team_players = await db_model.get_team_players(team_id=team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=team_id)

    captain = await db_model.get_player(team_player_captain.player_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    is_request_team = False

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            is_request_team = True

    players = []

    for team_player in team_players:
        if not team_player.is_captain:
            player = await db_model.get_player(player_id=team_player.player_id)
            players.append({
                'id': player.id,
                'username': player.username,
                'tg_username': player.tg_username,
                'is_ready': team_player.is_ready
            })

    team_composition_ikb = await team_kb.get_team_composition_ikb(players=players,
                                                                  captain=captain,
                                                                  is_captain=team_player.is_captain,
                                                                  is_request_team=is_request_team)

    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=team_composition_ikb)


# CAPTAIN FUNCTIONS
async def team_composition_captain(call: types.CallbackQuery, state: FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    team_kb = call.bot.get('kb').get('team')

    current_team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

    team_id = current_team_player.team_id

    team_players = await db_model.get_team_players(team_id=team_id)

    captain = await db_model.get_player_by_user_id(user_id=user_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    is_request_team = False

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            is_request_team = True

    players = []

    for team_player in team_players:
        if not team_player.is_captain:
            player = await db_model.get_player(player_id=team_player.player_id)
            players.append({
                'id': player.id,
                'username': player.username,
                'tg_username': player.tg_username,
                'is_ready': team_player.is_ready
            })

    team_composition_ikb = await team_kb.get_team_composition_ikb(players=players,
                                                                  captain=captain,
                                                                  is_captain=current_team_player.is_captain,
                                                                  is_request_team=is_request_team)

    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=team_composition_ikb)


def register_handlers_team_composition(dp: Dispatcher):
    dp.register_callback_query_handler(team_composition_captain, text=["team_composition"], state="*", is_captain=True)
    dp.register_callback_query_handler(team_composition, text=["team_composition"], state="*", is_team_player=True)
