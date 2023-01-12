import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.types.game.status import GameStatus
from tg_bot.types.match.status import MatchStatus
# choice game
# choice winner team


async def update_result_game(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    games = await db_model.get_games()

    if games is None:
        await call.answer('Активных игр, не найдено!')
        return

    games_data = []

    for game in games:
        match = await db_model.get_match(match_id=game.match_id)

        first_match_team = await db_model.get_tournament_team_by_id(tournament_team_id=match.first_tournament_team_id)
        second_match_team = await db_model.get_tournament_team_by_id(tournament_team_id=match.second_tournament_team_id)

        game_data = {
            'id': game.id,
            'first_match_team': first_match_team,
            'second_match_team': second_match_team,
        }

        games_data.append(game_data)

    choice_game_ikb = await admin_kb.get_choice_game_ikb(games=games_data)

    msg_text = '<b>Игра</b>\n\n' \
               'Выберите игру:'

    await call.message.answer(msg_text, reply_markup=choice_game_ikb)


async def choice_game(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    props = await parse_callback('choice_game', call.data)

    game_id = props.get('game_id')
    first_team_id = props.get('first_team_id')
    second_team_id = props.get('second_team_id')

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    first_team = await db_model.get_tournament_team_by_id(tournament_team_id=first_team_id)
    second_team = await db_model.get_tournament_team_by_id(tournament_team_id=second_team_id)

    choice_team_ikb = await admin_kb.get_choice_team_ikb(first_team=first_team, second_team=second_team, game_id=game_id)

    msg_text = '<b>Игра</b>\n\n' \
               'Выберите команду победителей'

    await call.message.answer(msg_text, reply_markup=choice_team_ikb)


async def choice_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    props = await parse_callback('choice_team', call.data)

    game_id = props.get('game_id')
    team_id = props.get('team_id')

    db_model = call.bot.get('db_model')

    game = await db_model.get_game(game_id=game_id)
    match = await db_model.get_match(match_id=game.match_id)

    position = 'second_tournament_team_id' if match.number_match % 2 == 0 else 'first_tournament_team_id'

    await db_model.match_set_tournament_team(team_id=team_id, position=position, number_match=match.next_number_match)
    await db_model.update_result_game(game_id=game_id, winner_team_id=team_id)
    await db_model.set_game_status(game_id=game_id, status=GameStatus.FINISH)
    await db_model.set_match_status(match_id=game.match_id, status=MatchStatus.FINISH)

    if match.stage != 'FINAL':
        next_match = await db_model.get_match_by_number_match(number_match=match.next_number_match)

        if next_match.first_tournament_team_id and next_match.second_tournament_team_id:
            await db_model.set_match_status(match_id=next_match.id, status=MatchStatus.TEAM_COMPLETE)


    await call.message.answer('Результаты игры, успешно обновлены')


def register_handlers_update_result_game(dp: Dispatcher):
    dp.register_callback_query_handler(update_result_game, text=['update_result_game'], state='*')
    dp.register_callback_query_handler(choice_game, text_contains=['choice_game'], state='*')
    dp.register_callback_query_handler(choice_team, text_contains=['choice_team'], state='*')
