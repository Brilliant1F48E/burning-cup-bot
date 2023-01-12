from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.misc.phares import Phrases


async def menu_players(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    answer_text = Phrases.players_title

    players_ikb = await admin_kb.get_players_ikb()

    await call.message.answer(
        text=answer_text,
        reply_markup=players_ikb
    )


async def view_all_players(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    players = await db_model.get_players()

    if len(players) == 0:
        answer_text = Phrases.teams_title + 'Ещё ни один игрок не зарегистрирован'

        await call.message.answer(
            text=answer_text,
        )
        return

    answer_text = Phrases.players_title
    players_ikb = await admin_kb.get_menu_view_all_players(players=players)

    await call.message.answer(
        text=answer_text,
        reply_markup=players_ikb
    )


async def view_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')


def register_handlers_menu_players(dp: Dispatcher):
    dp.register_callback_query_handler(menu_players, text=['player'], state='*')
