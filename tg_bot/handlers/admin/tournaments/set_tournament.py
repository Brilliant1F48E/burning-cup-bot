from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases


async def set_tournament(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')

    set_tournament_ikb = await admin_kb.get_set_tournament_ikb()

    answer_text = Phrases.tournament_title + Phrases.choice_action

    await call.message.answer(answer_text, reply_markup=set_tournament_ikb)


async def set_limit_teams(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


async def enter_limit_teams(msg: types.Message, state=FSMContext):
    pass


async def set_anons_date(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


async def enter_anons_date(msg: types.Message, state=FSMContext):
    pass


async def set_tournament_status(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


async def choice_tournament_status(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


async def confirm_set_tournament_status(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


def register_handlers_set_tournament(dp: Dispatcher):
    pass
