from aiogram.dispatcher.filters import BoundFilter


class MemberFilter(BoundFilter):
    key = 'is_member'

    def __init__(self, is_member=None):
        self.is_member = is_member

    async def check(self, obj):
        if self.is_member is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        member_exist = await db_model.is_member(user_id=user_id)

        return self.is_member == member_exist
