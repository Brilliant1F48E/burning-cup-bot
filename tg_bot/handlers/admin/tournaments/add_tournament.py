import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.tournament import AddTournament, TournamentStatus, TournamentPhrases
from tg_bot.misc.is_number import is_number


# Назначить турнир -> ввести название турнира -> ввести лимит команд -> ввести дату анонса (?дату анонса можно будет отредактировать)
async def add_tournament(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    answer_text = TournamentPhrases.title + TournamentPhrases.enter_tournament_name
    await call.message.answer(answer_text)

    await state.set_state(AddTournament.ENTER_NAME_TOURNAMENT)


async def enter_name_tournament(msg: types.Message, state=FSMContext):
    tournament_name = msg.text

    async with state.proxy() as data:
        data['tournament_name'] = tournament_name

    answer_text = TournamentPhrases.title + TournamentPhrases.enter_limit_teams
    await msg.answer(answer_text)

    await AddTournament.next()


async def enter_limit_teams(msg: types.Message, state=FSMContext):
    limit_teams = msg.text

    # проверка на число

    if not await is_number(limit_teams):
        return

    async with state.proxy() as data:
        data['limit_teams'] = limit_teams

    answer_text = TournamentPhrases.title + TournamentPhrases.enter_date_anons
    await msg.answer(answer_text)

    await AddTournament.next()


async def enter_date_anons(msg: types.Message, state=FSMContext):
    date_anons_text = msg.text

    if not date_anons_text:
        return msg.answer('Введите корректную дату')

    # проверка на корректность введённой даты

    date_and_time = date_anons_text.split('@')

    date = date_and_time[0].split(':')
    time = date_and_time[1].split(':')

    date_anons = datetime.datetime(day=int(date[0]), month=int(date[1]), year=int(date[2]),
                                   hour=int(time[0]),
                                   minute=int(time[1]))

    # (datetime.datetime.now() < date_anons)

    state_data = await state.get_data()
    db_model = msg.bot.get('db_model')

    tournament_name = state_data.get('tournament_name')
    limit_teams = state_data.get('limit_teams')

    await db_model.add_tournament(name=tournament_name, limit_teams=limit_teams, date_anons=date_anons)

    msg_text = TournamentPhrases.title + TournamentPhrases.msg_success

    await msg.answer(msg_text)
    await state.finish()


def register_handlers_add_tournament(dp: Dispatcher):
    dp.register_callback_query_handler(add_tournament, text=['set_tournament'], state='*', is_admin=True)
    dp.register_message_handler(enter_name_tournament, state=AddTournament.ENTER_NAME_TOURNAMENT, is_admin=True)
    dp.register_message_handler(enter_limit_teams, state=AddTournament.ENTER_LIMIT_TEAMS, is_admin=True)
    dp.register_message_handler(enter_date_anons, state=AddTournament.ENTER_DATE_ANONS, is_admin=True)
