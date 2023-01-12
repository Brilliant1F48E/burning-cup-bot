from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases


async def menu_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    tournament = await db_model.get_tournament()

    if tournament is None:
        return

    registration = await db_model.get_registration(tournament_id=tournament.id)

    registration_ikb = await admin_kb.get_registration_ikb(registration=registration)

    answer_text = Phrases.menu_registration + Phrases.choice_action

    await call.message.answer(text=answer_text,
                              reply_markup=registration_ikb)


async def back_to_registration(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    tournament = await db_model.get_tournament()

    if tournament is None:
        return

    registration = await db_model.get_registration(tournament_id=tournament.id)

    registration_ikb = await admin_kb.get_registration_ikb(registration=registration)

    answer_text = Phrases.menu_registration + Phrases.choice_action

    await call.bot.edit_message_text(
        text=answer_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=registration_ikb)


def register_handlers_menu_registration(dp: Dispatcher):
    dp.register_callback_query_handler(menu_registration, text=['registration'], state='*', is_admin=True)
    dp.register_callback_query_handler(back_to_registration, text=['back_to_registration'], state='*', is_admin=True)
