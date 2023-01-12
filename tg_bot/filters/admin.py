from aiogram.dispatcher.filters import BoundFilter

from tg_bot.config import Config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin=None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False

        config: Config = obj.bot.get('config')
        return (obj.from_user.id == config.tg_bot.admin_id) == self.is_admin
