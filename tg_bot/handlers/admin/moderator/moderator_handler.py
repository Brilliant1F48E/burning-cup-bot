import datetime
import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.moderator import VerifRequestMember
from tg_bot.types.request import RequestStatus
from tg_bot.types.member import MemberType
from tg_bot.types.registration import RegistrationStatus
from tg_bot.types.moderator import VerifRequestTeam

from tg_bot.misc.matches import grouping, add_matches
from tg_bot.misc.scripts import parse_callback, notify_user
from .menu import register_handler_menu


async def view_request_member(call: types.CallbackQuery):
    await call.answer(' ')

    bot = call.bot
    db_model = bot.get('db_model')
    moderator_kb = bot.get('kb').get('moderator')

    call_data = call.data

    props = await parse_callback('view_request_member', call_data)

    request_member_user_id = props.get('user_id')

    print(request_member_user_id)
    request_member = await db_model.get_request_member(user_id=request_member_user_id)

    # if request_member.request_member_status == RequestStatus.PROCESS:
    #     await call.message.answer('Анкета уже находится в процессе верификации')
    #     return
    if request_member.request_member_status == RequestStatus.SUCCESS or request_member.request_member_status == RequestStatus.FAIL:
        await call.message.answer('Анкета уже рассмотрена!')
        await call.message.delete()
        return

    await db_model.set_request_member_status(user_id=request_member_user_id, status=RequestStatus.PROCESS)

    actions_verif_ikb = await moderator_kb.get_actions_verif_ikb(user_id=request_member_user_id)

    member_type = request_member.member_type

    student_msg_text = f'<b>Верификация студента.</b>\n\n' \
                       f'ФИО: {request_member.first_name} {request_member.last_name} {request_member.patronymic}\n' \
                       f'Учебное заведение: {request_member.institution}\n' \
                       f'Группа: {request_member.group}'
    schoolboy_msg_text = f'<b>Верификация школьника.</b>\n\n' \
                         f'ФИО: {request_member.first_name} {request_member.last_name} {request_member.patronymic}\n' \
                         f'Учебное заведение: {request_member.institution}\n' \
                         f'Класс: {request_member.group}'
    msg_text = student_msg_text if member_type == MemberType.STUDENT else schoolboy_msg_text
    await bot.send_photo(chat_id=call.message.chat.id, photo=request_member.document_photo,
                         caption=msg_text,
                         reply_markup=actions_verif_ikb)


async def verif_request_member(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')

    bot = call.bot
    db_model = bot.get('db_model')

    call_data = call.data

    props = await parse_callback('verif_request_member', call_data)

    request_member_user_id = props.get('user_id')
    request_member_result = props.get('result')
    if request_member_result == 'no':
        await call.message.answer('Введите причину отказа:')
        await state.set_state(VerifRequestMember.ENTER_RESPONSE)

        async with state.proxy() as data:
            data['user_id'] = request_member_user_id
    elif request_member_result == 'yes':
        await call.message.delete()
        await db_model.set_request_member_status(user_id=request_member_user_id, status=RequestStatus.SUCCESS)
        request_member = await db_model.get_request_member(user_id=request_member_user_id)
        await db_model.add_member(user_id=request_member.user_id, first_name=request_member.first_name,
                                  last_name=request_member.last_name, patronymic=request_member.patronymic,
                                  institution=request_member.institution, member_type=request_member.member_type,
                                  group=request_member.group)

        register_kb = call.bot.get('kb').get('register')

        register_ikb = await register_kb.get_register_ikb()

        await notify_user(bot=call.bot, text='<b>✅ Верификация успешно пройдена!</b>',
                               chat_id=request_member_user_id,
                               reply_markup=register_ikb)


async def enter_comment_request_student(msg: types.Message, state=FSMContext):
    response_verif_request = msg.text

    state_data = await state.get_data()

    db_model = msg.bot.get('db_model')
    request_user_id = state_data.get('user_id')

    await db_model.set_request_member_status(user_id=request_user_id, status=RequestStatus.FAIL)
    await db_model.set_request_member_comment(user_id=request_user_id, comment=response_verif_request)
    register_kb = msg.bot.get('kb').get('register')
    repeated_request_member_ikb = await register_kb.get_repeated_request_member_ikb()
    await notify_user(bot=msg.bot, text=f'<b>❌ Вы не прошли верификацию</b>\n\n'
                                             f'<b>По причине:</b>\n{response_verif_request}', chat_id=request_user_id,
                           reply_markup=repeated_request_member_ikb)

    await state.finish()


async def view_request_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await state.finish()
    await call.message.delete()

    db_model = call.bot.get('db_model')
    moderator_kb = call.bot.get('kb').get('moderator')

    props = await parse_callback('view_request_team', call.data)

    team_id = props.get('team_id')

    team = await db_model.get_team(team_id=team_id)

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    # if request_team.request_status != RequestStatus.WAIT:
    #     await call.message.answer('Анкета уже верифицируется.')
    #     return

    await db_model.set_request_team_status(request_team_id=request_team.id, status=RequestStatus.PROCESS)
    verif_request_team_ikb = await moderator_kb.get_verif_request_team_ikb(request_team_id=request_team.id)

    team_players = await db_model.get_team_players(team_id=request_team.team_id)

    caption = '<b>Верификация команды</b>\n\n' \
              f'Название команды: <code>{team.name}</code>\n\n'

    for team_player in team_players:
        player = await db_model.get_player(player_id=team_player.player_id)

        caption += f'{player.discord}\n'

    caption += f'<b>Верифицировать команду?</b>'

    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo=team.photo_telegram_id,
        caption=caption,
        reply_markup=verif_request_team_ikb
    )


async def verif_request_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.delete()

    db_model = call.bot.get('db_model')

    props = await parse_callback('verif_request_team', call.data)

    request_team_id = props.get('request_team_id')
    result = props.get('result')

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    if result == 'yes':
        if registration.registration_status == RegistrationStatus.OPEN:
            request_team = await db_model.get_request_team(request_team_id=request_team_id)

            captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
            team_players = await db_model.get_team_players_without_captain(team_id=request_team.team_id,
                                                                           captain_id=captain.id)

            team = await db_model.get_team(team_id=request_team.team_id)

            photo_name = team.name + ".png"
            photo_telegram_id = team.photo_telegram_id
            file = await call.bot.get_file(photo_telegram_id)
            file_path = file.file_path

            directory = call.bot.get("config").get("path").get("images")
            path = os.path.join(directory, photo_name)

            await call.bot.download_file(file_path=file_path, destination_dir=path)

            await db_model.set_team_photo(team_id=team.id, photo=photo_name)

            await db_model.add_tournament_team(
                captain_id=captain.id,
                players=team_players,
                name=team.name,
                photo=photo_name,
            )

            tournament_teams = await db_model.get_tournament_teams()

            if len(tournament_teams) == tournament.limit_teams:
                await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CLOSE)

                closing_date = datetime.datetime.now()
                await db_model.set_registration_closing_date(registration_id=registration.id, closing_date=closing_date)
                users = await db_model.get_users()

                await db_model.set_request_team_status(request_team_id=request_team_id, status=RequestStatus.SUCCESS)

                player_captain = await db_model.get_player(player_id=captain.player_id)
                member_captain = await db_model.get_member(member_id=player_captain.member_id)

                await notify_user(
                    text='✅ Ваша команда приняла участие в турнире <b>🔥 Burning Cup</b>',
                    chat_id=member_captain.user_id,
                    bot=call.bot
                )

                await grouping(db_model=db_model)
                await add_matches(db_model=db_model)

                for user in users:
                    await notify_user(
                        text='Регистрация на турнир закончена <b>🔥 Burning Cup</b>\n\n'
                             'Команды и матчи можете посмотреть на сайте https://www.burning-cup.com',
                        chat_id=user.id,
                        bot=call.bot
                    )
    else:
        await call.message.answer('Введите причину отказа')
        await state.set_state(VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM)
        async with state.proxy() as data:
            data['request_team_id'] = request_team_id


async def enter_comment_request_team(msg: types.Message, state=FSMContext):
    comment = msg.text

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()

    request_team_id = state_data.get('request_team_id')

    await db_model.set_request_team_status(request_team_id=request_team_id, status=RequestStatus.FAIL)
    await db_model.set_request_team_comment(request_team_id=request_team_id, comment=comment)
    request_team = await db_model.get_request_team(request_team_id=request_team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
    player = await db_model.get_player(player_id=team_player_captain.player_id)
    member = await db_model.get_member(member_id=player.member_id)

    message_text = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                   'По причине:\n' \
                   f'{request_team.comment}'

    await notify_user(
        chat_id=member.user_id,
        text=message_text,
        bot=msg.bot
    )


def register_handlers_moderator(dp: Dispatcher):
    register_handler_menu(dp)
    dp.register_callback_query_handler(view_request_member, text_contains=['view_request_member'],
                                       is_moderator=True)
    dp.register_callback_query_handler(verif_request_member, text_contains=['verif_request_member'], state='*',
                                       is_moderator=True)
    dp.register_message_handler(enter_comment_request_student, state=VerifRequestMember.ENTER_RESPONSE,
                                is_moderator=True)
    dp.register_callback_query_handler(verif_request_team, text_contains=['verif_request_team'], state='*',
                                       is_moderator=True)
    dp.register_message_handler(enter_comment_request_team, state=VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM,
                                is_moderator=True)
