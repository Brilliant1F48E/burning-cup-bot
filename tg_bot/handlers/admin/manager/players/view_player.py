from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback
from tg_bot.types.member import MemberType


async def view_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(" ")
    await state.finish()

    props = await parse_callback("view_player", callback_data=call.data)

    player_id = props.get("player_id")
    db_model = call.bot.get("db_model")
    admin_kb = call.bot.get("kb").get("admin")

    player = await db_model.get_player(player_id=player_id)
    member = await db_model.get_member(member_id=player.member_id)
    request_member = await db_model.get_request_member(user_id=member.user_id)

    member_type = "Школьник" if member.member_type == MemberType.SCHOOLBOY else "Студент"
    group = "Класс" if member.member_type == MemberType.SCHOOLBOY else "Группа"

    caption = "<b>Просмотр игрока</b>\n\n" \
                  f"Тип: {member_type}\n" \
                  f"Фамилия: {member.last_name}\n" \
                  f"Имя: {member.first_name}\n" \
                  f"Отчество: {member.patronymic}\n" \
                  f"{group}: {member.group}\n" \
                  f"Учебное учреждение: {member.institution}\n" \
                  f"Псевдоним: {player.username}\n" \
                  f"Дискорд: {player.discord}\n" \
                  f"Фасткап: {player.fastcup}\n" \

    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=request_member.document_photo,
        caption=caption
    )


def register_handlers_view_player(dp: Dispatcher):
    dp.register_callback_query_handler(view_player, text_contains=["view_player"], state="*")
