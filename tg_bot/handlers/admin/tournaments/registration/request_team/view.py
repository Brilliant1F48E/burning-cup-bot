import aiogram.utils.markdown as fmt

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback


async def view(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")
    db_model = bot.get("db_model")

    props = await parse_callback("view_team_request", call.data)

    request_team_id = props.get("team_request_id")

    request_team = await db_model.get_request_team(request_team_id=request_team_id)

    team = await db_model.get_team(team_id=request_team.team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=team.id)

    player_captain = await db_model.get_player(player_id=team_player_captain.player_id)

    team_players = await db_model.get_team_players_without_captain(team_id=team.id,
                                                                   captain_id=team_player_captain.id)

    captain_text = fmt.text("<code>", fmt.quote_html(player_captain.username), "</code>", "<code>",
                            fmt.quote_html(player_captain.discord), "</code>\n")

    players_text = ""

    for team_player in team_players:
        player = await db_model.get_player(player_id=team_player.player_id)

        players_text += fmt.text("<code>", fmt.quote_html(player.username), "</code>", "<code>",
                                 fmt.quote_html(player.discord), "</code>\n")

    caption = "<b>Запрос команды</b>\n\n" \
              f"Статус: {request_team.request_status}\n" \
              f"Дата подачи: {request_team.date_request}\n" \
              f"Название команды: <code>{team.name}</code>\n\n" \
              f"Состав команды:\n\n" + captain_text + players_text

    moderation_request_team_ikb = await admin_kb.get_moderation_request_team_ikb(request_team_id=request_team.id)

    await bot.send_photo(
        chat_id=call.from_user.id,
        caption=caption,
        photo=team.photo_telegram_id,
        reply_markup=moderation_request_team_ikb
    )


def register_handlers_view(dp: Dispatcher):
    dp.register_callback_query_handler(menu_view_all_team_requests, text=["view_all_team_requests"], state="*",
                                       is_admin=True)
    dp.register_callback_query_handler(menu_view_team_request, text_contains=["view_team_request"], state="*",
                                       is_admin=True)
