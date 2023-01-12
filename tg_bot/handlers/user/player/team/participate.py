from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import check_rule_team_player, notify_moderators

from tg_bot.types.registration import RegistrationStatus
from tg_bot.misc.phares import Phrases
from tg_bot.types.request import RequestStatus

from tg_bot.types.moderator import ModeratorRule


async def participate(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()
    await call.message.delete()

    user_id = call.from_user.id
    db_model = call.bot.get("db_model")

    if not await check_rule_team_player(call=call):
        return

    team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

    if request_team:
        if request_team.request_status == RequestStatus.FAIL:
            if request_team.request_status == RequestStatus.SUCCESS:
                answer_text = "Вы уже приняли участие в турнире"
                await call.message.answer(text=answer_text)
                return
            elif request_team.request_status == RequestStatus.WAIT:
                answer_text = "Ваша анкета в ожидании верификации"
                await call.message.answer(text=answer_text)
                return
            elif request_team.request_status == RequestStatus.PROCESS:
                answer_text = "Ваша анкета верифицируется"
                await call.message.answer(text=answer_text)
                return
    
    if await db_model.is_tournament():
        tournament = await db_model.get_tournament()

        registration = await db_model.get_registration(tournament_id=tournament.id)

        if registration.registration_status == RegistrationStatus.CLOSE:
            await call.message.delete()

            text = "К сожалению регистрация уже закрыта. Вам обязательно повезёт в следующий раз."
            await call.message.answer(text=text)
            return
        elif registration.registration_status == RegistrationStatus.OPEN:
            current_team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

            if current_team_player.is_captain:
                team_id = current_team_player.team_id

                team_players = await db_model.get_team_players(team_id=team_id)

                if len(team_players) != 5:
                    await call.message.answer("Для участия в турнире необходимо 5 игроков.")
                    return

                for team_player in team_players:
                    print(team_player.is_ready)
                    if not team_player.is_ready:
                        await call.message.answer("Все игроки команды должны подтвердить готовность.")
                        return

                text = Phrases.notify_new_team
                moderator_kb = call.bot.get("kb").get("moderator")

                view_request_team_ikb = await moderator_kb.get_view_request_team_ikb(team_id=team_id)

                await db_model.add_request_team(team_id=team_id)

                answer_text = "Ваша анкета успешно отправлена на модерацию"

                await call.message.answer(text=answer_text)

                await notify_moderators(text=text,
                                        rule=ModeratorRule.VERIF_TEAM,
                                        bot=call.bot,
                                        kb=view_request_team_ikb)


def register_handlers_participate(dp: Dispatcher):
    dp.register_callback_query_handler(participate, text=["participate"], state="*", is_captain=True)
