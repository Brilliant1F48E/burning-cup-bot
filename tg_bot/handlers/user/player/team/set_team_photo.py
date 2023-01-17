from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import check_rule_team_player
from tg_bot.types.request import RequestStatus
from tg_bot.types.team.states import SetTeamPhoto


async def set_team_photo(call: types.CallbackQuery, state=FSMContext):
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
            answer_text = 'Во время верификации команды, менять название или изображение команды запрещено'
            await call.message.answer(answer_text)
            return

    answer_text = 'Отправьте новое фото команды:'
    await call.message.answer(answer_text)
    await state.set_state(SetTeamPhoto.SEND_NEW_TEAM_PHOTO)
    async with state.proxy() as data:
        data['team_id'] = team_player.team_id


async def send_new_team_photo(msg: types.Message, state=FSMContext):
    photo_telegram_id = msg.photo[-1].file_id

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()
    team_id = state_data.get('team_id')

    await db_model.set_team_photo_telegram_id(team_id=team_id, photo_telegram_id=photo_telegram_id)

    await msg.answer('Вы успешно изменили фотографию команды.')

    await state.finish()


def register_handlers_set_team_photo(dp: Dispatcher):
    dp.register_callback_query_handler(set_team_photo, text_contains=['set_team_photo'], state='*', is_captain=True)
    dp.register_message_handler(send_new_team_photo, state=SetTeamPhoto.SEND_NEW_TEAM_PHOTO,
                                content_types=types.ContentType.PHOTO)
