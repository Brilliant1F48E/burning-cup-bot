from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import check_rule_team_player


async def confirm_ready(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id

    db_model = call.bot.get("db_model")

    if not await check_rule_team_player(call=call):
        return

    team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

    if team_player.is_ready:
        await call.message.answer("Вы уже подтвердили свою готовость.")
        return

    await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=True)

    await call.message.answer("Вы успешно подтвердили свою готовость.")


def register_handlers_confirm_ready(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_ready, text=["confirm_ready"], state="*", is_team_player=True)
