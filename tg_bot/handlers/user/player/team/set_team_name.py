from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import check_rule_team_player
from tg_bot.types.request import RequestStatus
from tg_bot.types.team.states import SetTeamName


async def set_team_name(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await state.finish()

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    if not await check_rule_team_player(call=call):
        return

    team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            answer_text = 'Во время верификации команды запрещено: менять название, изображение или расформировывать команду!'
            await call.message.answer(answer_text)
            return

    answer_text = 'Введите новое имя команды:'
    await call.message.answer(answer_text)
    await state.set_state(SetTeamName.ENTER_NEW_TEAM_NAME)
    async with state.proxy() as data:
        data['team_id'] = team_player.team_id


async def enter_new_team_name(msg: types.Message, state=FSMContext):
    new_team_name = msg.text

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()
    team_id = state_data.get('team_id')

    if await db_model.is_valid_team_name(name=new_team_name):
        await msg.answer('Такое название уже используется.')
        return

    await db_model.set_team_name(team_id=team_id, name=new_team_name)

    await msg.answer('Вы успешно изменили название команды.')

    await state.finish()


def register_handlers_set_team_name(dp: Dispatcher):
    dp.register_callback_query_handler(set_team_name, text_contains=['set_team_name'], state='*', is_captain=True)
    dp.register_message_handler(enter_new_team_name, state=SetTeamName.ENTER_NEW_TEAM_NAME)