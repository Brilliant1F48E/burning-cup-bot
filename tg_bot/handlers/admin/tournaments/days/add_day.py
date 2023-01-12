from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.types.days.states import AddDay
from tg_bot.types.game.status import GameStatus


async def add_day(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    game = await db_model.get_next_game()

    day_title = '<b>День</b>\n\n'
    text = 'Выберите команду:'
    msg_text = day_title + text

    if game is None:
        text = 'Игра ещё не назначена'
        msg_text = day_title + text
        await call.message.answer(msg_text)
        return

    match = await db_model.get_match(match_id=game.match_id)

    first_tournament_team = await db_model.get_tournament_team_by_id(tournament_team_id=match.first_tournament_team_id)
    second_tournament_team = await db_model.get_tournament_team_by_id(tournament_team_id=match.second_tournament_team_id)

    game_data = {
        'id': game.id,
        'first_tournament_team': first_tournament_team,
        'second_tournament_team': second_tournament_team,
    }

    add_day_choice_game_ikb = await admin_kb.get_add_day_choice_game_ikb(game=game_data)

    await call.message.answer(text=msg_text,
                              reply_markup=add_day_choice_game_ikb)
    await state.set_state(AddDay.CHOICE_GAME)


async def choice_game(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')

    props = await parse_callback('add_day_choice_game', call.data)

    game_id = props.get('game_id')

    async with state.proxy() as data:
        data['game_id'] = game_id

    day_title = '<b>День</b>\n\n'
    text = 'Отправьте ссылку на стрим:'

    msg_text = day_title + text

    await call.message.answer(msg_text)
    await AddDay.next()


async def send_stream_link(msg: types.Message, state=FSMContext):
    response_msg_text = msg.text

    state_data = await state.get_data()

    db_model = msg.bot.get('db_model')
    game_id = state_data.get('game_id')

    await db_model.set_game_status(game_id=game_id, status=GameStatus.ONLINE)
    await db_model.add_day(game_id=game_id, stream_link=response_msg_text)

    day_title = '<b>День</b>\n\n'
    text = 'День успешно создан'
    msg_text = day_title + text

    await msg.answer(msg_text)
    await state.finish()


def register_handlers_add_day(dp: Dispatcher):
    dp.register_callback_query_handler(add_day, text=["add_day"], state='*', is_admin=True)
    dp.register_callback_query_handler(choice_game, state=AddDay.CHOICE_GAME, is_admin=True)
    dp.register_message_handler(send_stream_link, state=AddDay.ENTER_STREAM_LINK, is_admin=True)
