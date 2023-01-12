from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.tournament import TournamentPhrases


async def menu_management(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    menu_tournament_management_ikb = await admin_kb.get_menu_tournament_management_ikb(registration=registration)

    answer_text = TournamentPhrases.title + 'Выберите действие:'

    await call.message.answer(text=answer_text, reply_markup=menu_tournament_management_ikb)


def register_handlers_menu_management(dp: Dispatcher):
    dp.register_callback_query_handler(menu_management, text=['tournament_management'], state='*')
