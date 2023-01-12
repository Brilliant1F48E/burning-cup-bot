from aiogram.dispatcher.filters import BoundFilter


class CaptainFilter(BoundFilter):
    key = 'is_captain'

    def __init__(self, is_captain=None):
        self.is_captain = is_captain

    async def check(self, obj):
        if self.is_captain is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        if not await db_model.is_team_player(user_id=user_id):
            return False

        team_player = await db_model.get_team_player_by_user_id(user_id=user_id)

        return self.is_captain == team_player.is_captain
