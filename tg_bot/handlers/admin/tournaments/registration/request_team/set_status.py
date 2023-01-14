from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.types.request import RequestStatus


async def set_request_team_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()
    await call.message.delete()

    bot = call.bot
    props = await parse_callback("set_request_team_status", call.data)
    db_model = bot.get("db_model")
    request_team_id = props.get("request_team_id")

    await db_model.set_request_team_status(request_team_id=request_team_id, request_status=RequestStatus.SUCCESS)

    answer_text = "Статус запроса команды успешно изменён на SUCCESS"

    await call.message.answer(answer_text)


def register_handlers_set_status(dp: Dispatcher):
    dp.register_callback_query_handler(set_request_team_status, text_contains=["set_request_team_status"], state="*", is_admin=True)
