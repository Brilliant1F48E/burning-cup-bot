import asyncio
import os

from aiogram import types, Bot
from aiogram.types import File

from tg_bot.misc.phares import Phrases
from tg_bot.types.team_player import TeamPlayerStatus


async def check_rule_team_player(call: types.CallbackQuery):
    user_id = call.from_user.id
    db_model = call.bot.get("db_model")
    team_kb = call.bot.get("kb").get("team")

    if await db_model.is_team_player(user_id=user_id):
        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

        team_ikb = await team_kb.get_team_ikb(team_exist=False)

        if team_player.team_player_status == TeamPlayerStatus.DISBANDED:
            answer_text = Phrases.menu_team + Phrases.disbanded_team

            await call.message.answer(answer_text, reply_markup=team_ikb)
            return
        elif team_player.team_player_status == TeamPlayerStatus.BANNED:
            answer_text = Phrases.menu_team + Phrases.banned_team

            await call.message.answer(answer_text, reply_markup=team_ikb)
            return
        elif team_player.team_player_status == TeamPlayerStatus.KICK:
            answer_text = Phrases.menu_team + Phrases.kick_from_team

            await call.message.answer(answer_text, reply_markup=team_ikb)
            return
        elif team_player.team_player_status == TeamPlayerStatus.LEAVE:
            answer_text = Phrases.menu_team + Phrases.leave_from_team

            await call.message.answer(answer_text)
            return

    return True


async def download_photo(bot: Bot, file_id: str, name: str) -> str:
    photo_file: File = await bot.get_file(file_id)
    file_ext: str = photo_file.file_path.split(".")[-1]
    photo_name: str = name + "." + file_ext
    images_path = bot.get("config").get("path").get("images")
    path: str = os.path.join(images_path, photo_name)

    await bot.download_file(file_path=photo_file.file_path, destination=path)

    return photo_name


async def parse_callback(method: str, callback_data) -> dict:
    data = callback_data.replace(f'{method}?', '')

    result = dict()

    if '&' in data:
        for item in data.split('&'):
            prop = item.split('=')
            result[prop[0]] = prop[1]
    else:
        prop = data.split('=')
        result[prop[0]] = prop[1]

    return result


async def notify_user(text: str, chat_id: int, bot, reply_markup=None, delay: float = 0):
    await asyncio.sleep(delay=delay)

    await bot.send_message(text=text, chat_id=chat_id, reply_markup=reply_markup)


async def notify_moderators(text: str, rule: str, bot, kb=None, delay: float = 0):
    await asyncio.sleep(delay=delay)

    db_model = bot.get('db_model')
    moderators = await db_model.get_moderators(rule=rule)

    if moderators is not None:
        for moderator in moderators:
            await bot.send_message(text=text, chat_id=moderator.user_id, reply_markup=kb)