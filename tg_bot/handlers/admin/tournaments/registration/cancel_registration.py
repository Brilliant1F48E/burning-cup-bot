from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.registration.status import RegistrationStatus


async def cancel_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CANCEL)
    await call.bot.edit_message_text(
        text='Регистрация успешно отменена',
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )


def register_handlers_cancel_registration(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_registration, text=['cancel_registration'], state='*', is_admin=True)

