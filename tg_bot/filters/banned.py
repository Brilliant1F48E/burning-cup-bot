from aiogram.dispatcher.filters import BoundFilter

from tg_bot.types.member import MemberStatus


class BannedFilter(BoundFilter):
    key = 'is_banned'

    def __init__(self, is_banned=None):
        self.is_banned = is_banned

    async def check(self, obj):
        if self.is_banned is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        if not await db_model.is_team_player(user_id=user_id):
            return False

        banned = False

        if await db_model.is_member(user_id=user_id):
            member = await db_model.get_member_by_user_id(user_id=user_id)
            banned = member.member_status == MemberStatus.BANNED

        return self.is_banned == banned
