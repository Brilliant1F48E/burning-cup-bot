from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards import RequestTeamKb
from tg_bot.misc.scripts import parse_callback


async def choice_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    props: dict = await parse_callback("choice_status", call.data)
    request_type: str = props.get("request_type")
    request_id: str = props.get("request_id")

    request_kb: RequestTeamKb = call.bot.get("kb").get("request").get("team")

    ikb_choice_status: types.InlineKeyboardMarkup = await request_kb.choice_status(
        request_type=request_type,
        request_id=request_id
    )

    answer_text: str = "<b>Запрос</b>\n\nВыберите статус:"

    await call.message.answer(
        text=answer_text,
        reply_markup=ikb_choice_status
    )


async def set_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()
    await call.answer(" ")
    await state.finish()

    bot: Bot = call.bot
    db_model = bot.get("db_model")

    props: dict = await parse_callback("choice_status", call.data)
    request_type: str = props.get("request_type")
    request_id: str = props.get("request_id")
    request_status: str = props.get("request_status")

    await db_model.set_request_team_status(request_team_id=request_id, request_status=request_status)

    answer_text: str = "<b>Статус запроса успешно изменён</b>"

    await call.message.answer(answer_text)


def register_handlers_set_status(dp: Dispatcher):
    dp.register_callback_query_handler(choice_status, text_contains=["choice_status"], state="*", is_admin=True)
    dp.register_callback_query_handler(set_status, text_contains=["set_status"], state="*", is_admin=True)
