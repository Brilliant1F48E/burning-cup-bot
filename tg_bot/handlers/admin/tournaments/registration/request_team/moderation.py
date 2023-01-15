import datetime
from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext

from tg_bot import DBInteraction
from tg_bot.misc.matches import add_matches, grouping
from tg_bot.misc.scripts import notify_user, parse_callback, download_photo
from tg_bot.models.db_model.models import TeamPlayer, RequestTeam, Team
from tg_bot.types.moderator import VerifRequestTeam
from tg_bot.types.registration import RegistrationStatus
from tg_bot.types.request import RequestStatus


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

    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    if request_status == RequestStatus.SUCCESS:
        if registration.registration_status == RegistrationStatus.OPEN:
            request_team: RequestTeam = await db_model.get_request_team(request_team_id=request_id)
            await db_model.set_request_team_status(request_team_id=request_id, request_status=RequestStatus.SUCCESS)

            captain: TeamPlayer = await db_model.get_captain_by_team_id(team_id=request_team.team_id)

            team_players: list = await db_model.get_team_players_without_captain(team_id=request_team.team_id,
                                                                                 captain_id=captain.id)

            team: Team = await db_model.get_team(team_id=request_team.team_id)

            photo_name: str = await download_photo(bot=bot, file_id=team.photo_telegram_id, name=team.name)

            await db_model.set_team_photo(team_id=team.id, photo=photo_name)

            await db_model.add_tournament_team(
                captain_id=captain.id,
                players=team_players,
                name=team.name,
                photo=photo_name,
            )

            player_captain = await db_model.get_player(player_id=captain.player_id)
            member_captain = await db_model.get_member(member_id=player_captain.member_id)

            await notify_user(
                text='✅ Ваша команда приняла участие в турнире <b>🔥 Burning Cup</b>',
                chat_id=member_captain.user_id,
                bot=call.bot
            )

            tournament_teams = await db_model.get_tournament_teams()

            if len(tournament_teams) == tournament.limit_teams:
                await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CLOSE)

                closing_date = datetime.datetime.now()
                await db_model.set_registration_closing_date(registration_id=registration.id, closing_date=closing_date)
                users = await db_model.get_users()

                await db_model.set_request_team_status(request_team_id=request_id, status=RequestStatus.SUCCESS)

                await grouping(db_model=db_model)
                await add_matches(db_model=db_model)

                for user in users:
                    await notify_user(
                        text='Регистрация на турнир закончена <b>🔥 Burning Cup</b>\n\n'
                             'Команды и матчи можете посмотреть на сайте https://www.burning-cup.com',
                        chat_id=user.id,
                        bot=call.bot
                    )
    elif request_status == RequestStatus.FAIL:
        await call.message.answer('Введите причину отказа')
        await state.set_state(VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM)
        async with state.proxy() as data:
            data['request_team_id'] = request_team_id


def register_handlers_moderation(dp: Dispatcher):
    dp.register_callback_query_handler(moderation, text=["moderation"], state="*", is_admin=True)
