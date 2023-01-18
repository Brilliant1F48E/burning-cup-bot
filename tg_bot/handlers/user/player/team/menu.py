from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player import TeamPlayerStatus

from tg_bot.misc.phares import Phrases

from tg_bot.misc.scripts import check_rule_team_player


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

    await state.finish()


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=["team", "back_to_team"], state="*", is_player=True)
