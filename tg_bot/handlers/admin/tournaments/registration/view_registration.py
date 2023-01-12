import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.registration import RegistrationStatus


async def view_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    opening_date = registration.opening_date

    msg_title_text = f'<b>Просмотр регистрации</b>\n\n'
    count_places_text = f'Кол-во мест: <code>{tournament.limit_teams}</code>\n'
    opening_date_text = f'Дата начала: <code>{opening_date}</code>\n'

    back_to_registration_ikb = await admin_kb.get_back_to_registration_ikb()

    if registration.registration_status == RegistrationStatus.WAIT:
        current_date = datetime.datetime.now()
        left_time = opening_date - current_date

        left_time_text = f'До начала регистрации осталось: <code>{left_time}</code>'

        msg_text = msg_title_text + count_places_text + opening_date_text + left_time_text

        await call.bot.edit_message_text(
            text=msg_text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_registration_ikb
        )
    elif registration.registration_status == RegistrationStatus.OPEN:
        count_tournament_teams = len(await db_model.get_tournament_teams())
        free_places_left = tournament.limit_teams - count_tournament_teams if count_tournament_teams is not None else tournament.limit_teams

        free_places_left_text = f'Свободных мест: <code>{free_places_left}</code>\n'
        msg_text = msg_title_text + count_places_text + free_places_left_text

        await call.bot.edit_message_text(
            text=msg_text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_registration_ikb
        )
    elif registration.registration_status == RegistrationStatus.CLOSE:
        msg_text = msg_title_text + 'Регистрация успешно завершена'
        await call.bot.edit_message_text(
            text=msg_text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_to_registration_ikb
        )


def register_handlers_view_registration(dp: Dispatcher):
    dp.register_callback_query_handler(view_registration, text=['view_registration'], state='*', is_admin=True)
