import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.types.game import AddGame
from tg_bot.types.match import MatchStatus


async def add_game(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')

    matches = await db_model.get_matches(match_status=MatchStatus.TEAM_COMPLETE)

    if matches is None:
        await call.message.answer('Нет матчей без даты')
        return

    matches_data = []

    for match in matches:
        first_match_team = await db_model.get_tournament_team_by_id(tournament_team_id=match.first_tournament_team_id)
        second_match_team = await db_model.get_tournament_team_by_id(tournament_team_id=match.second_tournament_team_id)

        match_data = {
            'id': match.id,
            'first_match_team': first_match_team,
            'second_match_team': second_match_team,
        }

        matches_data.append(match_data)

    admin_ikb = call.bot.get('kb').get('admin')

    add_game_ikb = await admin_ikb.get_add_game_ikb(matches=matches_data)

    await call.message.answer(f'<b>Игры</b>\n\n'
                              f'Выберите матч:',
                              reply_markup=add_game_ikb)


async def choice_match(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    props = await parse_callback('choice_match', call.data)

    match_id = props.get('match_id')

    msg_text = 'Напишити дату и время начала игры:' \
               'В формате day:month:year@hour:minute'

    await call.message.answer(text=msg_text)

    await state.set_state(AddGame.ENTER_DATE_START)
    print(match_id)
    async with state.proxy() as data:
        data['match_id'] = match_id


async def set_date(msg: types.Message, state=FSMContext):
    msg_text = msg.text

    if not msg_text:
        return msg.answer('Введите корректную дату')

    date_and_time = msg_text.split('@')

    data_date = date_and_time[0].split(':')
    data_time = date_and_time[1].split(':')

    start_date = datetime.datetime(day=int(data_date[0]), month=int(data_date[1]), year=int(data_date[2]),
                                     hour=int(data_time[0]),
                                     minute=int(data_time[1]))

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()

    match_id = state_data.get('match_id')
    print(match_id)
    print(start_date)
    await db_model.add_game(match_id=match_id, start_date=start_date)
    await state.finish()


def register_handlers_add_game(dp: Dispatcher):
    dp.register_callback_query_handler(add_game, text=['add_game'], state='*')
    dp.register_callback_query_handler(choice_match, text_contains=['choice_match'], state='*')
    dp.register_message_handler(set_date, state=AddGame.ENTER_DATE_START)
