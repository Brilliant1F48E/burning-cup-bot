from aiogram.dispatcher.filters import BoundFilter


class TeamPlayerFilter(BoundFilter):
    key = 'is_team_player'

    def __init__(self, is_team_player=None):
        self.is_team_player = is_team_player

    async def check(self, obj):
        if self.is_team_player is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        team_player_exist = await db_model.is_team_player(user_id=user_id)
        return self.is_team_player == team_player_exist
