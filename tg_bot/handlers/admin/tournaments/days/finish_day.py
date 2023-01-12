from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from tg_bot.types.days import DayStatus
from tg_bot.misc.phares import Phrases


async def finish_day(call: types.CallbackQuery, state: FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')

    answer_text = Phrases.day_title + Phrases.confirm_finish_day
    confirm_finish_day_ikb = await admin_kb.get_confirm_finish_day_ikb()

    await call.message.answer(text=answer_text,
                              reply_markup=confirm_finish_day_ikb)


async def confirm_finish_day(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')

    day = await db_model.get_day()
    await db_model.set_day_status(day_id=day.id, status=DayStatus.FINISH)

    answer_text = Phrases.day_title + Phrases.success_finish_day

    await call.message.answer(text=answer_text)


def register_handlers_finish_day(dp: Dispatcher):
    dp.register_callback_query_handler(finish_day, text=['finish_day'], state='*')
    dp.register_callback_query_handler(confirm_finish_day, text=['confirm_finish_day'], state='*')