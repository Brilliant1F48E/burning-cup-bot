from aiogram import Dispatcher, types

from tg_bot.misc.generate_invite_code import generate_invite_code
from tg_bot.misc.scripts import check_rule_team_player, parse_callback
from tg_bot.models.db_model.models import TeamPlayer


async def team_invite_code(call: types.CallbackQuery):
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')
    team_kb = call.bot.get('kb').get('team')

    if not await check_rule_team_player(call=call):
        return

    team_player: TeamPlayer = await db_model.get_team_player_by_user_id(user_id=user_id)
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


def register_handlers_invite_code(dp: Dispatcher):
    dp.register_callback_query_handler(team_invite_code, text=["invite_code"], state='*',
                                       is_team_player=True, is_captain=True)
    dp.register_callback_query_handler(team_generate_invite_code, text_contains=['generate_invite_code'],
                                       state='*',
                                       is_team_player=True, is_captain=True)
