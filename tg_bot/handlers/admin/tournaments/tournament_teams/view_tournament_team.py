from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.parse import parse_callback


# Заблокировать команду
# Снять с турнира
# Показать участников
async def view_tournament_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    props = await parse_callback('view_tournament_team', call.data)

    tournament_team_id = props.get('tournament_team_id')

    tournament_team = await db_model.get_tournament_team(tournament_team_id=tournament_team_id)

    menu_tournament_teams_ikb = await admin_kb.get_view_tournament_team_ikb(tournament_teams=tournament_team)

    msg_title_text = '<b>Турнирные команды</b>\n\n'

    await call.bot.edit_message_text(
        text=msg_title_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=menu_tournament_teams_ikb
    )


def register_handlers_view_tournament_team(dp: Dispatcher):
    dp.register_callback_query_handler(view_tournament_team, text='view_tournament_team', state='*')
