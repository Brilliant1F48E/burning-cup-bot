from aiogram.dispatcher.filters import BoundFilter


class PlayerFilter(BoundFilter):
    key = 'is_player'

    def __init__(self, is_player=None):
        self.is_player = is_player

    async def check(self, obj):
        if self.is_player is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        player_exist = await db_model.is_player(user_id=user_id)
        return self.is_player == player_exist
