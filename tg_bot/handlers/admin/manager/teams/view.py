from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


from tg_bot.misc.scripts import parse_callback
from tg_bot.models.db_model.models import Team


async def view_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    props = await parse_callback("view_team", call.data)

    team_id = props.get("team_id")

    admin_kb = call.bot.get("kb").get("admin")

    db_model = call.bot.get("db_model")

    team: Team = await db_model.get_team(team_id=team_id)

    team_players = await db_model.get_team_players_by_team_id(team_id=team_id)

    players = []
    captain = None

    for team_player in team_players:
        if team_player.is_captain:
            captain = await db_model.get_player(player_id=team_player.player_id)
        else:
            players.append(await db_model.get_player(player_id=team_player.player_id))

    view_team_ikb = await admin_kb.get_view_team_ikb(players=players, captain=captain, team_id=team_id)

    caption: str = "<b>Просмотр команды</b>\n\n" \
              f"Название команды: <code>{team.name}</code>\n" \
              "Состав команды:"

    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=team.photo_telegram_id,
        caption=caption,
        reply_markup=view_team_ikb
    )


def register_handlers_view(dp: Dispatcher):
    dp.register_callback_query_handler(view_team, text_contains=["view_team"], state="*", is_admin=True)
