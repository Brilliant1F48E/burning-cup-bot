from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback, notify_user
from tg_bot.misc.phares import Phrases

from tg_bot.types.team import TeamStatus
from tg_bot.types.player import PlayerStatus
from tg_bot.types.team_player import TeamPlayerStatus
from tg_bot.types.member import MemberStatus


async def menu_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    teams = await db_model.get_teams()

    if len(teams) == 0:
        answer_text = Phrases.teams_title + 'Ещё ни одна команда не зарегистрирована'

        await call.message.answer(
            text=answer_text,
        )
        return

    team_ikb = await admin_kb.get_menu_teams_ikb(teams=teams)

    answer_text = Phrases.teams_title

    await call.message.answer(
        text=answer_text,
        reply_markup=team_ikb
    )


async def view_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    props = await parse_callback("view_team", call.data)

    team_id = props.get("team_id")

    admin_kb = call.bot.get("kb").get("admin")

    db_model = call.bot.get("db_model")

    team = await db_model.get_team(team_id=team_id)

    team_players = await db_model.get_team_players_by_team_id(team_id=team_id)

    players = []
    captain = None

    for team_player in team_players:
        if team_player.is_captain:
            captain = await db_model.get_player(player_id=team_player.player_id)
        else:
            players.append(await db_model.get_player(player_id=team_player.player_id))

    view_team_ikb = await admin_kb.get_view_team_ikb(players=players, captain=captain, team_id=team_id)

    caption = "<b>Просмотр команды</b>\n\n" \
              f"Название команды: <code>{team.name}</code>\n" \
              "Состав команды:"

    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=team.photo_telegram_id,
        caption=caption,
        reply_markup=view_team_ikb
    )


async def banned_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    props = await parse_callback("banned_team", call.data)
    team_id = props.get("team_id")
    db_model = call.bot.get("db_model")

    team = await db_model.get_team(team_id=team_id)

    team_players = await db_model.get_team_players_by_team_id(team_id=team.id)

    for team_player in team_players:
        player = await db_model.get_player(player_id=team_player.player_id)
        member = await db_model.get_member(member_id=player.member_id)

        await db_model.set_player_status(player_id=player.id, status=PlayerStatus.BANNED)
        await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.BANNED)
        await db_model.set_member_status(member_id=member.id, status=MemberStatus.BANNED)
        text_banned = "<b>Бан</b>\n\n" \
                      "Вы были навсегда заблокированы.\n" \
                      "По причине:\n" \
                      "Нарушение пункта Регламента 3.6 - Наличие в логотипе команды нецензурных графических изображений"
        await notify_user(text_banned,
                          chat_id=member.user_id,
                          bot=call.bot)

    await db_model.set_team_status(team_id=team_id, status=TeamStatus.BANNED)


def register_handlers_menu_teams(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=["teams"], state="*", is_admin=True)
    dp.register_callback_query_handler(view_team, text_contains=["view_team"], state="*", is_admin=True)
    dp.register_callback_query_handler(banned_team, text_contains=["banned_team"], state="*", is_admin=True)
