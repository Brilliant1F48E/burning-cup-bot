from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


# Показать все турнирные команды
async def menu_tournament_teams(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    tournament_teams = await db_model.get_tournament_teams()
    msg_title_text = '<b>Турнирные команды</b>\n\n'

    if len(tournament_teams) == 0:
        msg_text = msg_title_text + 'Ещё ни одна команда на одобренна на турнир'
        await call.bot.edit_message_text(
            text=msg_text,
            message_id=call.message.message_id,
            chat_id=call.message.chat.id,
        )
        return

    menu_tournament_teams_ikb = await admin_kb.get_menu_tournament_teams_ikb(tournament_teams=tournament_teams)

    await call.bot.edit_message_text(
        text=msg_title_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=menu_tournament_teams_ikb
    )



def register_handlers_menu_tournament_teams(dp: Dispatcher):
    dp.register_callback_query_handler(menu_tournament_teams, text='tournament_teams', state='*')
