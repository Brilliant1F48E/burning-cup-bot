from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def games(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_ikb = call.bot.get('kb').get('admin')

    games_ikb = await admin_ikb.get_games_ikb()

    await call.message.answer('<b>Игры</b>\n\n'
                              'Выберите действие',
                              reply_markup=games_ikb)


def register_handlers_menu_games(dp: Dispatcher):
    dp.register_callback_query_handler(games, text=['games'], state='*')
