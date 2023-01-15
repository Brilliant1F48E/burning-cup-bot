import aiogram.utils.markdown as fmt

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards import RequestTeamKb
from tg_bot.misc.scripts import parse_callback
from tg_bot.models.db_model.models import RequestTeam, Team, TeamPlayer, Player
from tg_bot.types.request import RequestStatus


async def view(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    request_kb: RequestTeamKb = bot.get("kb").get("request").get("team")
    db_model = bot.get("db_model")

    props: dict = await parse_callback("view", call.data)

    request_id = props.get("id")
    request_type = props.get("type")
    request_status = props.get("status")

    request: RequestTeam = await db_model.get_request_team(request_team_id=request_id)
    team: Team = await db_model.get_team(team_id=request.team_id)
    team_player_captain: TeamPlayer = await db_model.get_captain_by_team_id(team_id=team.id)
    player_captain: TeamPlayer = await db_model.get_player(player_id=team_player_captain.player_id)
    team_players: list = await db_model.get_team_players_without_captain(team_id=team.id,
                                                                         captain_id=team_player_captain.id)
    request_title: str = request_type == "team" if "<b>Запрос команды</b>\n\n" else "<b>Запрос пользователя</b>\n\n"

    request_info: str = f"Тип: {request_type}\n" \
                        f"Статус: {request_status}\n" \
                        f"Дата: {request.date_request}\n" \
                        f"Название команды: <code>{fmt.quote_html(team.name)}</code>\n" \
                        f"Состав команды:\n\n"

    captain_text: str = fmt.text("<code>", fmt.quote_html(player_captain.username), "</code>", "<code>",
                                 fmt.quote_html(player_captain.discord), "</code>\n")

    team_composition: str = captain_text

    for team_player in team_players:
        player: Player = await db_model.get_player(player_id=team_player.player_id)
        player_text: str = fmt.text("<code>", fmt.quote_html(player.username), "</code>", "<code>",
                                    fmt.quote_html(player.discord), "</code>\n")
        team_composition += player_text

    caption: str = request_title + request_info + team_composition

    ikb_view: types.InlineKeyboardMarkup = await request_kb.view(request_type=request_type,
                                                                 request_id=request_id,
                                                                 request_status=request_status)

    if request_status == RequestStatus.WAIT or request_status == RequestStatus.PROCESS:
        pass

    await bot.send_photo(
        chat_id=call.from_user.id,
        caption=caption,
        photo=team.photo_telegram_id,
        reply_markup=ikb_view
    )


def register_handlers_view(dp: Dispatcher):
    dp.register_callback_query_handler(view, text_contains=["view"], state="*",
                                       is_admin=True)
