from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.misc.phares import Phrases


async def menu_days(call: types.CallbackQuery, state: FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    answer_text = Phrases.day_title + Phrases.choice_action

    day = await db_model.get_day()

    menu_days_ikb = await admin_kb.get_menu_days_ikb(day)

    await call.message.answer(text=answer_text,
                              reply_markup=menu_days_ikb)


def register_handlers_menu_days(dp: Dispatcher):
    dp.register_callback_query_handler(menu_days, text=['days'], state='*', is_admin=True)
