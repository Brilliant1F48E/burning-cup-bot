from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.tournament import TournamentPhrases


async def menu_tournaments(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    tournament = await db_model.get_tournament()

    registration = None

    if tournament:
        registration = await db_model.get_registration(tournament_id=tournament.id)

    menu_tournaments_ikb = await admin_kb.get_tournament_ikb(tournament=tournament, registration=registration)

    answer_text = TournamentPhrases.title + TournamentPhrases.menu_tournament

    await call.message.answer(text=answer_text, reply_markup=menu_tournaments_ikb)


def register_handlers_menu_tournaments(dp: Dispatcher):
    dp.register_callback_query_handler(menu_tournaments, text=['tournaments'], state='*')
