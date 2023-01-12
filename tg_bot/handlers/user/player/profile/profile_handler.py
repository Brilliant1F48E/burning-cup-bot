from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.request import RequestStatus
from tg_bot.misc.phares import Phrases
from tg_bot.types.team_player import SetFastcup, SetDiscord, SetUsername


async def profile(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(" ")

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")

    player = await db_model.get_player_by_user_id(user_id=user_id)

    profile_kb = call.bot.get("kb").get("profile")

    if await db_model.is_team_player(user_id=user_id):
        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
        team = await db_model.get_team(team_id=team_player.team_id)

        answer_text = Phrases.menu_profile + f'<b>Команда</b>: <code>{team.name}</code>\n' \
                                             f'<b>Псевдоним</b>: <code>{player.username}</code>\n' \
                                             f'<b>Дискорд</b>: <code>{player.discord}</code>\n' \
                                             f'<b>Фасткап</b>: <code>{player.fastcup}</code>'
    else:
        answer_text = Phrases.menu_profile + f'<b>Псевдоним</b>: <code>{player.username}</code>\n' \
                                             f'<b>Дискорд</b>: <code>{player.discord}</code>\n' \
                                             f'<b>Фасткап</b>: <code>{player.fastcup}</code>'

    profile_ikb = await profile_kb.get_profile_ikb()

    await call.bot.edit_message_text(
        text=answer_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=profile_ikb
    )


async def set_username(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    if await db_model.is_team_player(user_id=user_id):
        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        if request_team:
            if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
                answer_text = Phrases.team_player_verification_block

                await call.message.answer(answer_text)
                return

    answer_text = Phrases.enter_new_username
    await call.message.answer(answer_text)
    await state.set_state(SetUsername.ENTER_NEW_USERNAME)


async def enter_new_username(msg: types.Message, state=FSMContext):
    username = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_username(username=username):
        answer_text = Phrases.username_already_in_use
        await msg.answer(answer_text)
        return

    await db_model.set_player_username(user_id=msg.from_user.id, username=username)

    answer_text = Phrases.username_success_changed
    await msg.answer(answer_text)
    await state.finish()


async def set_fastcup(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")

    if await db_model.is_team_player(user_id=user_id):
        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        if request_team:
            if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
                answer_text = Phrases.team_player_verification_block

                await call.message.answer(answer_text)
                return

    answer_text = Phrases.enter_new_fastcup

    await call.message.answer(answer_text)
    await state.set_state(SetFastcup.ENTER_NEW_FASTCUP)


async def enter_new_fastcup(msg: types.Message, state=FSMContext):
    fastcup = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_fastcup(fastcup=fastcup):
        answer_text = Phrases.fastcup_already_in_use

        await msg.answer(answer_text)
        return

    await db_model.set_player_fastcup(user_id=msg.from_user.id, fastcup=fastcup)

    answer_text = Phrases.fastcup_success_changed

    await msg.answer(answer_text)
    await state.finish()


async def set_discrod(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")

    if await db_model.is_team_player(user_id=user_id):
        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        if request_team:
            if request_team.request_status == RequestStatus.WAIT or request_team.request_status == RequestStatus.PROCESS:
                answer_text = Phrases.team_player_verification_block

                await call.message.answer(answer_text)
                return

    answer_text = Phrases.enter_new_discord

    await call.message.answer(answer_text)
    await state.set_state(SetDiscord.ENTER_NEW_DISCORD)


async def enter_new_discord(msg: types.Message, state=FSMContext):
    discord = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_discord(discord=discord):
        answer_text = Phrases.discord_already_in_use

        await msg.answer(answer_text)
        return

    await db_model.set_player_discord(user_id=msg.from_user.id, discord=discord)

    answer_text = Phrases.discord_success_changed

    await msg.answer(answer_text)
    await state.finish()


def register_handlers_profile(dp: Dispatcher):
    dp.register_callback_query_handler(profile, text=["profile"], is_player=True, state="*")

    dp.register_callback_query_handler(set_username, text=["set_username"], state='*', is_player=True)
    dp.register_message_handler(enter_new_username, state=SetUsername.ENTER_NEW_USERNAME, is_player=True)
    dp.register_callback_query_handler(set_fastcup, text=["set_fastcup"], state='*', is_player=True)
    dp.register_message_handler(enter_new_fastcup, state=SetFastcup.ENTER_NEW_FASTCUP, is_player=True)
    dp.register_callback_query_handler(set_discrod, text=["set_discord"], state='*', is_player=True)
    dp.register_message_handler(enter_new_discord, state=SetDiscord.ENTER_NEW_DISCORD, is_player=True)
