
from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from tg_bot.handlers.admin.requests.add_tournament_team import add_tournament_team
from tg_bot.handlers.admin.requests.close_registration import close_registration

from tg_bot.misc.scripts import notify_user, parse_callback
from tg_bot.models.db_model.models import TeamPlayer, RequestTeam, Tournament, Registration
from tg_bot.types.registration import RegistrationStatus
from tg_bot.types.request import RequestStatus
from tg_bot.types.request.states import ModerationRequestEnterComment


async def moderation(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer(" ")
    await state.finish()

    bot: Bot = call.bot
    props: dict = await parse_callback("moderation", call.data)
    request_type: str = props.get("type")
    request_id: str = props.get("id")
    request_status: str = props.get("status")

    db_model = bot.get("db_model")

    tournament: Tournament = await db_model.get_tournament()
    registration: Registration = await db_model.get_registration(tournament_id=tournament.id)

    if request_type == "team":
        if registration.registration_status == RegistrationStatus.CLOSE:
            await call.message.answer('Регистрация закрыта!')
            return

        if request_status == RequestStatus.SUCCESS:
            if registration.registration_status == RegistrationStatus.OPEN:
                request_team: RequestTeam = await db_model.get_request_team(request_team_id=request_id)
                await db_model.set_request_team_status(request_team_id=request_id, request_status=RequestStatus.SUCCESS)

                captain: TeamPlayer = await db_model.get_captain_by_team_id(team_id=request_team.team_id)

                await add_tournament_team(db_model=db_model, request_team=request_team, bot=bot, captain=captain)

                player_captain = await db_model.get_player(player_id=captain.player_id)
                member_captain = await db_model.get_member(member_id=player_captain.member_id)

                await notify_user(
                    text='✅ Ваша команда приняла участие в турнире <b>🔥 Burning Cup</b>',
                    chat_id=member_captain.user_id,
                    bot=call.bot
                )

                tournament_teams = await db_model.get_tournament_teams()

                if len(tournament_teams) == tournament.limit_teams:
                    await close_registration(db_model=db_model, bot=bot, registration=registration)

        elif request_status == RequestStatus.FAIL:
            await call.message.answer('Введите причину отказа')

            await state.set_state(ModerationRequestEnterComment.ENTER_COMMENT)
            async with state.proxy() as data:
                data['request_id'] = request_id
    else:
        if request_status == RequestStatus.FAIL:
            await call.message.answer('Введите причину отказа:')
            await state.set_state(ModerationRequestEnterComment.ENTER_COMMENT)

            async with state.proxy() as data:
                data['request_id'] = request_id
        elif request_status == RequestStatus.SUCCESS:
            await call.message.delete()
            await db_model.set_request_member_status(request_id=request_id, status=RequestStatus.SUCCESS)
            request_member = await db_model.get_request_member(request_id=request_id)
            await db_model.add_member(user_id=request_member.user_id, first_name=request_member.first_name,
                                      last_name=request_member.last_name, patronymic=request_member.patronymic,
                                      institution=request_member.institution, member_type=request_member.member_type,
                                      group=request_member.group)

            register_kb = call.bot.get('kb').get('register')

            register_ikb = await register_kb.get_register_ikb()

            notify_text: str = "<b>✅ Модерация успешно пройдена!</b>"
            await notify_user(bot=call.bot, text=notify_text,
                              chat_id=request_member.user_id,
                              reply_markup=register_ikb)


def register_handlers_moderation(dp: Dispatcher):
    dp.register_callback_query_handler(moderation, text_contains=["moderation"], state="*", is_admin=True)
