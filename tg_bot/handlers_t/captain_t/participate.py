import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.emoji import Emoji
from tg_bot.misc.notify import notify_moderators
from tg_bot.types.moderator import ModeratorRule
from tg_bot.types.registration import RegistrationStatus


async def get_declination_text(lacks):
    base_text = 'Вам не хватает'

    if lacks == 1:
        return f'{base_text} {lacks}-ого игрока.'
    elif lacks == 2:
        return f'{base_text} {lacks}-ух игроков.'
    else:
        return f'{base_text} {lacks}-ёх игроков.'


async def participate(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    current_team_player = await db_model.get_team_player(user_id=user_id)
    team_player_kb = call.bot.get('kb').get('team_player')
    team_players = await db_model.get_team_players(team_id=current_team_player.team_id)
    len_team_players = len(team_players)

    back_to_team_ikb = await team_player_kb.get_back_to_team_ikb()

    registration_title_text = f'<b>{Emoji.burn} Burning Cup</b>\n\n'

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    if registration.registration_status == RegistrationStatus.CLOSE:
        registration_close = 'Регистрация на турнир закончена.'
        msg_text = registration_title_text + registration_close

        await call.bot.edit_message_text(text=msg_text,
                                         chat_id=call.message.chat.id,
                                         message_id=call.message.message_id)
        return
    elif len_team_players != 5:
        lacks = 5 - len_team_players
        lacks_text = await get_declination_text(lacks=lacks)
        registration_not_enough_players_text = 'Для участие в турнире необходимо, иметь в команде 5 игроков.\n\n' \
                                               f'{lacks_text}'
        msg_text = registration_title_text + registration_not_enough_players_text

        await call.bot.edit_message_text(text=msg_text,
                                         chat_id=call.message.chat.id,
                                         message_id=call.message.message_id,
                                         reply_markup=back_to_team_ikb)
        return

    for team_player in team_players:
        if not team_player.is_participate and team_player.id != current_team_player.id:
            registration_confirm_participation = 'Для участие в турнире необходимо,' \
                                                 'чтобы каждый член команды подтвердил своё участие.'
            msg_text = registration_title_text + registration_confirm_participation

            await call.bot.edit_message_text(text=msg_text,
                                             chat_id=call.message.chat.id,
                                             message_id=call.message.message_id,
                                             reply_markup=back_to_team_ikb)
            return

    print(registration.registration_status)

    if registration.registration_status == RegistrationStatus.OPEN:
        registration_open = 'Все игроки команды подтвердили своё участие.\n\n' \
                            'Принять участие в турнире?'
        msg_text = registration_title_text + registration_open
        participate_ikb = await team_player_kb.get_confirm_participate_ikb()

        await call.bot.edit_message_text(text=msg_text,
                                         chat_id=call.message.chat.id,
                                         message_id=call.message.message_id,
                                         reply_markup=participate_ikb)


async def confirm_participate(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    moderator_kb = call.bot.get('kb').get('moderator')
    team_player = await db_model.get_team_player(user_id=user_id)

    await db_model.add_request_team(team_id=team_player.team_id)
    view_request_team_ikb = await moderator_kb.get_view_request_team_ikb(team_id=team_player.team_id)

    await notify_moderators(text='<b>🛎 Появилась новая команда</b>', rule=ModeratorRule.VERIF_TEAM,
                            kb=view_request_team_ikb, call=call)

    answer_text = 'Ваша заявка на участие в турнире отправлена на рассмотрение.\n' \
                  '🛎 Ожидайте уведомление.'

    await call.bot.edit_message_text(
        text=answer_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )


def register_handlers_participate(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_participate, text=['confirm_participate'], state='*', is_captain=True)
    dp.register_callback_query_handler(participate, text=['participate'], state='*', is_captain=True)
