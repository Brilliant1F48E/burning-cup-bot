from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases
from tg_bot.misc.scripts import parse_callback


async def menu_requests(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    admin_kb = call.bot.get("kb").get("admin")
    answer_text = Phrases.menu_requests + Phrases.choice_action

    menu_requests_ikb = await admin_kb.get_menu_requests_ikb()

    await call.message.answer(
        text=answer_text,
        reply_markup=menu_requests_ikb
    )


async def menu_member_request(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    admin_kb = call.bot.get("kb").get("admin")

    answer_text = Phrases.menu_requests + Phrases.choice_action

    member_requests = await admin_kb.get_member_requests_ikb()

    await call.message.answer(
        text=answer_text,
        reply_markup=member_requests
    )


async def view_member_requests(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    db_model = call.bot.get("db_model")
    admin_kb = call.bot.get("kb").get("admin")

    answer_text = Phrases.menu_requests + Phrases.choice_action

    member_requests = await db_model.get_member_requests()

    view_member_requests_ikb = await admin_kb.get_view_member_requests_ikb(member_requests)

    await call.message.answer(
        text=answer_text,
        reply_markup=view_member_requests_ikb
    )


def register_handlers_menu_requests(dp: Dispatcher):
    dp.register_callback_query_handler(menu_requests, text=["menu_requests"], state="*", is_admin=True)
    dp.register_callback_query_handler(menu_member_request, text=["member_requests"], state="*", is_admin=True)
    dp.register_callback_query_handler(view_member_requests, text=["view_member_requests"], state="*", is_admin=True)

