import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import notify_user
from tg_bot.misc.scheduler import scheduler
from tg_bot.types.registration import StartRegistrationStates, RegistrationStatus
from tg_bot.misc.phares import Phrases


# дата начала
async def start_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    msg_text = 'Напишити дату и время начала регистрации:' \
               'В формате day:month:year@hour:minute'

    await call.message.answer(text=msg_text)
    await state.set_state(StartRegistrationStates.ENTER_START_DATE)


async def enter_date_registration(msg: types.Message, state=FSMContext):
    msg_text = msg.text

    if not msg_text:
        await msg.answer('Введите корректную дату')
        return

    date_and_time = msg_text.split('@')

    if len(date_and_time) != 2:
        await msg.answer('Введите корректную дату')
        return

    data_date = date_and_time[0].split(':')

    if len(data_date) != 3:
        await msg.answer('Введите корректную дату')
        return

    data_time = date_and_time[1].split(':')

    if len(data_time) != 2:
        await msg.answer('Введите корректную дату')
        return

    opening_date = datetime.datetime(day=int(data_date[0]), month=int(data_date[1]), year=int(data_date[2]),
                                   hour=int(data_time[0]),
                                   minute=int(data_time[1]))

    current_date = datetime.datetime.now()

    # проверить является ли дата актуальной
    bot = msg.bot
    db_model = bot.get('db_model')
    tournament = await db_model.get_tournament()

    registration = await db_model.add_registration(opening_date=opening_date, tournament_id=tournament.id)

    date_left = opening_date - current_date

    answer_text = Phrases.menu_registration + Phrases.registration_success_add + f"Дата: <code>{opening_date}</code>\n" \
                                                                                 f"До начала: <code>{date_left}</code>"

    await msg.answer(answer_text)

    msg_text = Phrases.registration_is_open

    date_left_in_second = date_left.total_seconds()

    await state.finish()

    teams = await db_model.get_teams_active()

    await scheduler(db_model.set_registration_status, date_left_in_second, registration.id, RegistrationStatus.OPEN)

    for team in teams:
        captain = await db_model.get_captain_by_team_id(team_id=team.id)
        player = await db_model.get_player(player_id=captain.player_id)
        member = await db_model.get_member(member_id=player.member_id)
        await notify_user(delay=date_left_in_second, text=msg_text, chat_id=member.user_id, bot=bot)


def register_handlers_start_registration(dp: Dispatcher):
    dp.register_callback_query_handler(start_registration, text=['open_registration'], state='*', is_admin=True)
    dp.register_message_handler(enter_date_registration, state=StartRegistrationStates.ENTER_START_DATE, is_admin=True)
