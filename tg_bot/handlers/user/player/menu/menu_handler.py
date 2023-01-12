from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.player import PlayerStatus

from tg_bot.misc.phares import Phrases


async def menu(msg: types.Message, state=FSMContext):
    await state.finish()

    user_id = msg.from_user.id
    db_model = msg.bot.get("db_model")
    menu_kb = msg.bot.get("kb").get("menu")
    register_kb = msg.bot.get("kb").get("register")

    player = await db_model.get_player_by_user_id(user_id=user_id)

    if msg.text != '💠 Меню':
        start_ikb = await register_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=start_ikb)

    if player.player_status == PlayerStatus.BANNED:
        message_text = Phrases.player_banned
        await msg.answer(message_text)
    elif player.player_status == PlayerStatus.ACTIVE:
        menu_ikb = await menu_kb.get_menu_ikb()

        answer_text = Phrases.menu + Phrases.choice_action
        await msg.answer(text=answer_text, reply_markup=menu_ikb)


async def menu_call(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(" ")

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")
    menu_kb = call.bot.get("kb").get("menu")

    player = await db_model.get_player_by_user_id(user_id=user_id)

    if player.player_status == PlayerStatus.BANNED:
        # Инлайн клавиатура с кнопкой обжаловать
        message_text = Phrases.player_banned
        await call.message.answer(message_text)
    elif player.player_status == PlayerStatus.ACTIVE:
        menu_ikb = await menu_kb.get_menu_ikb()

        answer_text = Phrases.menu + Phrases.choice_action
        await call.message.answer(text=answer_text, reply_markup=menu_ikb)


async def back_to_menu(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()
    await call.message.delete()

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")
    menu_kb = call.bot.get("kb").get("menu")
    register_kb = call.bot.get("kb").get("register")

    player = await db_model.get_player_by_user_id(user_id=user_id)

    if player.player_status == PlayerStatus.BANNED:
        # Инлайн клавиатура с кнопкой обжаловать
        message_text = Phrases.player_banned
        await call.message.answer(message_text)
    elif player.player_status == PlayerStatus.ACTIVE:
        menu_ikb = await menu_kb.get_menu_ikb()

        answer_text = Phrases.menu + Phrases.choice_action
        await call.message.answer(text=answer_text, reply_markup=menu_ikb)


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_menu, text=["back_to_menu"], is_player=True, state="*")
    dp.register_message_handler(menu, commands=["start"], is_player=True, state="*")
    dp.register_message_handler(menu, text="💠 Меню", is_player=True, state="*")
    dp.register_callback_query_handler(menu_call, text="menu", is_player=True, state="*")
