from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from tg_bot.types.team_player import TeamPlayerStatus
from tg_bot.misc.generate_invite_code import generate_invite_code

from tg_bot.types.request import RequestStatus
from tg_bot.misc.phares import Phrases
from tg_bot.types.team import TeamStatus

from tg_bot.misc.scripts import parse_callback, notify_user, check_rule_team_player, notify_moderators


class SetTeamName(StatesGroup):
    ENTER_NEW_TEAM_NAME = State()


class SetTeamPhoto(StatesGroup):
    SEND_NEW_TEAM_PHOTO = State()


async def menu_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')
    await call.message.delete()

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")
    team_kb = call.bot.get("kb").get("team")

    team_ikb = await team_kb.get_team_ikb(team_exist=False)

    if await db_model.is_team_player(user_id=user_id):
        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

        if not await check_rule_team_player(call=call):
            return

        if team_player.team_player_status == TeamPlayerStatus.ACTIVE:

            team_ikb = await team_kb.get_team_ikb(team_exist=True)

            team = await db_model.get_team(team_id=team_player.team_id)

            if team_player.is_captain:
                registration = None

                if await db_model.is_registration():
                    tournament = await db_model.get_tournament()
                    registration = await db_model.get_registration(tournament_id=tournament.id)

                request_team = await db_model.get_request_team_by_team_id(team_id=team.id)

                team_ikb = await team_kb.get_team_ikb(team_exist=True, is_captain=team_player.is_captain,
                                                      registration=registration,
                                                      is_ready=team_player.is_ready,
                                                      request_team=request_team)

            caption_text = Phrases.menu_team + f'<b>Имя команды</b>: <code>{team.name}</code>\n'

            await call.bot.send_photo(chat_id=call.message.chat.id,
                                      photo=team.photo_telegram_id,
                                      caption=caption_text,
                                      reply_markup=team_ikb)
            return

    answer_text = Phrases.menu_team + Phrases.not_team

    await call.message.answer(answer_text, reply_markup=team_ikb)


# TEAM PLAYER FUNCTIONS
async def leave_the_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    team_kb = call.bot.get('kb').get('team')

    confirm_leave_the_team_ikb = await team_kb.get_confirm_leave_the_team_ikb()
    db_model = call.bot.get('db_model')

    team_player = await db_model.get_team_player(user_id=call.from_user.id)

    if not await check_rule_team_player(call=call):
        return

    if team_player:
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        if request_team:
            if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
                answer_text = Phrases.team_player_verification_block
                await call.message.answer(answer_text)
                return

    answer_text = Phrases.confirm_leave_from_team
    await call.message.answer(answer_text, reply_markup=confirm_leave_the_team_ikb)


async def confirm_leave_the_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    team_player = await db_model.get_team_player(user_id=user_id)
    await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.LEAVE)

    await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=False)

    answer_text = Phrases.success_leave_from_team
    await call.message.answer(answer_text)


async def team_invite_code(call: types.CallbackQuery):
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')
    team_kb = call.bot.get('kb').get('team')

    if not await check_rule_team_player(call=call):
        return

    team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
    team_id = team_player.team_id
    invite_code = await db_model.get_invite_code(team_id=team_id)

    generate_invite_code_ikb = await team_kb.get_generate_invite_code_ikb(team_id=team_id)
    await call.bot.edit_message_caption(caption=f'<b>💠 Комадна</b>\n\n'
                                                f'<b>Код приглашения:</b>\n\n'
                                                f'<code>{invite_code}</code>',
                                        message_id=call.message.message_id,
                                        chat_id=call.message.chat.id,
                                        reply_markup=generate_invite_code_ikb)


async def team_generate_invite_code(call: types.CallbackQuery):
    await call.answer(' ')

    if not await check_rule_team_player(call=call):
        return
    db_model = call.bot.get('db_model')
    team_kb = call.bot.get('kb').get('team')
    call_data = call.data
    props = await parse_callback('generate_invite_code', callback_data=call_data)
    team_id = props.get('team_id')

    invite_code = await generate_invite_code()

    while await db_model.is_valid_invite_code(invite_code=invite_code):
        invite_code = await generate_invite_code()

    await db_model.set_invite_code(team_id=team_id, invite_code=invite_code)

    generate_invite_code_ikb = await team_kb.get_generate_invite_code_ikb(team_id=team_id)
    await call.bot.edit_message_caption(caption=f'<b>💠 Комадна</b>\n\n'
                                                f'<b>Код приглашения:</b>\n\n'
                                                f'<code>{invite_code}</code>',
                                        message_id=call.message.message_id,
                                        chat_id=call.message.chat.id,
                                        reply_markup=generate_invite_code_ikb)


async def disband_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    team_kb = call.bot.get('kb').get('team')
    db_model = call.bot.get("db_model")

    if not await check_rule_team_player(call=call):
        return

    team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
    team_id = team_player.team_id

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            answer_text = Phrases.captain_verification_block
            await call.message.answer(answer_text)
            return

    confirm_disband_team_ikb = await team_kb.get_confirm_disband_team(team_id=team_id)

    caption = Phrases.confirm_disband_team

    await call.bot.edit_message_caption(caption=caption,
                                        message_id=call.message.message_id,
                                        chat_id=call.message.chat.id,
                                        reply_markup=confirm_disband_team_ikb)


async def confirm_disband_team(call: types.CallbackQuery):
    await call.answer(' ')
    await call.message.delete()

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    props = await parse_callback('confirm_disband_team', call.data)

    team_id = props.get('team_id')

    captain_team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
    await db_model.set_team_player_is_ready(team_player_id=captain_team_player.id, is_ready=False)

    team_players = await db_model.get_team_players(team_id=team_id)

    for team_player in team_players:
        await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.DISBANDED)
        await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=False)
        await db_model.set_is_captain(team_player_id=team_player.id, is_captain=False)

    await db_model.set_team_status(team_id=team_id, status=TeamStatus.DISBANDED)

    answer_text = Phrases.success_disband_team

    await call.message.answer(text=answer_text, reply_markup=None)


async def kick_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    team_kb = call.bot.get('kb').get('team')
    db_model = call.bot.get('db_model')

    if not await check_rule_team_player(call=call):
        return

    current_team_player = await db_model.get_team_player_by_user_id(user_id=call.from_user.id)

    request_team = await db_model.get_request_team_by_team_id(team_id=current_team_player.team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
            answer_text = Phrases.captain_verification_block
            await call.message.answer(answer_text)
            return

    props = await parse_callback(method='kick_team_player', callback_data=call.data)
    player_id = props.get('player_id')

    confirm_kick_team_player_ikb = await team_kb.get_confirm_kick_team_player_ikb(player_id=player_id)
    player = await db_model.get_player(player_id=player_id)

    answer_text = Phrases.confirm_kick_team_player + f' {player.username}?'

    await call.message.answer(answer_text, reply_markup=confirm_kick_team_player_ikb)


async def confirm_kick_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    props = await parse_callback(method='confirm_kick_team_player', callback_data=call.data)
    player_id = props.get('player_id')

    team_player = await db_model.get_team_player_by_player_id(player_id=player_id)

    await db_model.set_team_player_status_by_player_id(team_player_id=team_player.id, status=TeamPlayerStatus.KICK)
    await db_model.set_team_player_is_ready(team_player_id=team_player.id, is_ready=False)

    answer_text = Phrases.success_kick_team_player

    player = await db_model.get_player(player_id=player_id)
    member = await db_model.get_member(member_id=player.member_id)

    await notify_user(text=Phrases.kick_from_team, bot=call.bot, chat_id=member.user_id)
    await call.message.answer(answer_text)


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


def register_team_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=["team", "back_to_team"], state="*", is_player=True)

    dp.register_callback_query_handler(confirm_ready, text=["confirm_ready"], state="*", is_team_player=True)

    # CAPTAIN FUNCTIONS

    dp.register_callback_query_handler(team_invite_code, text=["invite_code"], state='*',
                                       is_team_player=True, is_captain=True)
    dp.register_callback_query_handler(team_generate_invite_code, text_contains=['generate_invite_code'],
                                       state='*',
                                       is_team_player=True, is_captain=True)
    dp.register_callback_query_handler(disband_team, text=["disband_team"], state='*', is_captain=True)

    dp.register_callback_query_handler(confirm_disband_team, text_contains=['confirm_disband_team'],
                                       is_captain=True)

    dp.register_callback_query_handler(confirm_kick_player, text_contains=['confirm_kick_team_player'], state='*',
                                       is_captain=True)
    dp.register_callback_query_handler(kick_player, text_contains=['kick_team_player'], state='*',
                                       is_captain=True)

    dp.register_callback_query_handler(set_team_photo, text_contains=['set_team_photo'], state='*', is_captain=True)
    dp.register_message_handler(send_new_team_photo, state=SetTeamPhoto.SEND_NEW_TEAM_PHOTO,
                                content_types=types.ContentType.PHOTO)

    dp.register_callback_query_handler(set_team_name, text_contains=['set_team_name'], state='*', is_captain=True)
    dp.register_message_handler(enter_new_team_name, state=SetTeamName.ENTER_NEW_TEAM_NAME)

    dp.register_callback_query_handler(confirm_leave_the_team, text_contains=['confirm_leave_the_team'], state='*',
                                       is_team_player=True)
    dp.register_callback_query_handler(leave_the_team, text_contains=['leave_the_team'], state='*',
                                       is_team_player=True)

    # PLAYER FUNCTIONS
