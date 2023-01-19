from tg_bot.misc.scripts import download_photo
from tg_bot.models.db_model.models import TeamPlayer, RequestTeam, Team, Player
from aiogram import Bot


async def add_tournament_team(db_model, request_team: RequestTeam, bot: Bot, captain: TeamPlayer):
    team_players: list = await db_model.get_team_players_without_captain(team_id=request_team.team_id,
                                                                         captain_id=captain.id)

    team: Team = await db_model.get_team(team_id=request_team.team_id)

    photo_name: str = await download_photo(bot=bot, file_id=team.photo_telegram_id, name=team.name)

    await db_model.set_team_photo(team_id=team.id, photo=photo_name)

    await db_model.add_tournament_team(
        captain_id=captain.player_id,
        players=team_players,
        name=team.name,
        photo=photo_name,
    )
