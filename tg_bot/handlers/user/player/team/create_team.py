from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.player import CreateTeam

from tg_bot.misc.generate_invite_code import generate_invite_code


async def create_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    await call.message.answer('Введите название команды:')
    await state.set_state(CreateTeam.ENTER_TEAM_NAME)


async def enter_name_team(msg: types.Message, state=FSMContext):
    team_name = msg.text

    db_model = msg.bot.get('db_model')

    if await db_model.is_valid_team_name(name=team_name):
        await msg.answer('Данное название уже занято!')
        return

    async with state.proxy() as data:
        data['team_name'] = team_name

    await msg.answer('Отправьте фото команды:')
    await CreateTeam.next()


async def send_team_photo(msg: types.Message, state=FSMContext):
    db_model = msg.bot.get('db_model')

    user_id = msg.from_user.id

    state_data = await state.get_data()
    team_name = state_data.get('team_name')

    photo_telegram_id = msg.photo[-1].file_id

    invite_code = await generate_invite_code()

    while await db_model.is_valid_invite_code(invite_code=invite_code):
        invite_code = await generate_invite_code()

    team = await db_model.add_team(name=team_name, photo_telegram_id=photo_telegram_id,
                                   invite_code=invite_code)

    await db_model.add_team_player(user_id=user_id, team_id=team.id, is_captain=True)

    await msg.answer('✅ Команда успешно создана!')
    await state.finish()


def register_handlers_create_team(dp: Dispatcher):
    dp.register_callback_query_handler(create_team, text=['create_team'], state='*', is_player=True)
    dp.register_message_handler(enter_name_team, state=CreateTeam.ENTER_TEAM_NAME, is_player=True)
    dp.register_message_handler(send_team_photo, state=CreateTeam.SEND_TEAM_PHOTO,
                                content_types=types.ContentType.PHOTO, is_player=True)
