from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.player import JoinTeam


async def join_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    await call.message.answer('Введите код приглашения:')
    await state.set_state(JoinTeam.ENTER_INVITE_CODE)


async def enter_join_code(msg: types.Message, state=FSMContext):
    invite_code = msg.text
    user_id = msg.from_user.id
    db_model = msg.bot.get('db_model')

    if not await db_model.is_valid_invite_code(invite_code=invite_code):
        await msg.answer('Некорректный код приглашения!')
        return

    team = await db_model.get_team_by_invite_code(invite_code=invite_code)
    team_players = await db_model.get_team_players(team_id=team.id)
    len_team_players = len(team_players)

    if len_team_players >= 5:
        await msg.answer('Команда уже сформированна!')
        return

    await db_model.add_team_player(user_id=user_id, team_id=team.id, is_captain=False)
    await msg.answer('Вы успешно присоеденились к команде!')
    await state.finish()


def register_handlers_join_team(dp: Dispatcher):
    dp.register_callback_query_handler(join_team, text=['join_team'], state='*', is_player=True)
    dp.register_message_handler(enter_join_code, state=JoinTeam.ENTER_INVITE_CODE, is_player=True)