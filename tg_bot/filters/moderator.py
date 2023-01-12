from aiogram.dispatcher.filters import BoundFilter


class ModeratorFilter(BoundFilter):
    key = 'is_moderator'

    def __init__(self, is_moderator=None):
        self.is_moderator = is_moderator

    async def check(self, obj):
        if self.is_moderator is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        moderator_exist = await db_model.moderator_exist(user_id=user_id)

        return self.is_moderator == moderator_exist
