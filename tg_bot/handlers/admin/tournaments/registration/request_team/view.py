import aiogram.utils.markdown as fmt

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.keyboards import RequestTeamKb
from tg_bot.misc.scripts import parse_callback
from tg_bot.models.db_model.models import RequestTeam, Team, TeamPlayer, Player
from tg_bot.types.member import MemberType
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

    if request_type == "team":
        request: RequestTeam = await db_model.get_request_team(request_team_id=request_id)
        team: Team = await db_model.get_team(team_id=request.team_id)
        team_player_captain: TeamPlayer = await db_model.get_captain_by_team_id(team_id=team.id)
        player_captain: TeamPlayer = await db_model.get_player(player_id=team_player_captain.player_id)
        team_players: list = await db_model.get_team_players_without_captain(team_id=team.id,
                                                                             captain_id=team_player_captain.id)
        request_title: str = "<b>Запрос команды</b>\n\n"

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

        caption = request_title + request_info + team_composition
        photo_id = team.photo_telegram_id
    else:
        request_member = await db_model.get_request_member(request_id=request_id)

        # if request_member.request_member_status == RequestStatus.PROCESS:
        #     await call.message.answer('Анкета уже находится в процессе верификации')
        #     return

        # await db_model.set_request_member_status(user_id=request_member_user_id, status=RequestStatus.PROCESS)
        request_title: str = "<b>Запрос студента</b>\n\n" if request_member.member_type == MemberType.STUDENT else "<b>Запрос школьника</b>\n\n"
        request_group: str = f"Группа: {request_member.group}" if request_member.member_type == MemberType.STUDENT else f"Класс: {request_member.group}"
        request_fullname: str = f"ФИО: {request_member.first_name} {request_member.last_name} {request_member.patronymic}\n"
        request_institution: str = f"Учебное заведение: {request_member.institution}\n"
        caption = request_title + request_fullname + request_institution + request_group
        photo_id: str = request_member.document_photo

    ikb_view: types.InlineKeyboardMarkup = await request_kb.view(request_type=request_type,
                                                                 request_id=request_id,
                                                                 request_status=request_status)
    await bot.send_photo(
        chat_id=call.from_user.id,
        caption=caption,
        photo=photo_id,
        reply_markup=ikb_view
    )


def register_handlers_view(dp: Dispatcher):
    dp.register_callback_query_handler(view, text_contains=["view"], state="*", is_admin=True)
