from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tg_bot.keyboards.base_kb import BaseKb


class ProfileKb(BaseKb):
    ib_set_username = InlineKeyboardButton('👤 Изменить псевдоним', callback_data='set_username')
    ib_set_fastcup = InlineKeyboardButton('🏆 Изменить фасткап', callback_data='set_fastcup')
    ib_set_discord = InlineKeyboardButton('📞 Изменить дискорд', callback_data='set_discord')

    async def get_profile_ikb(self, is_blocking_changes: bool = False):
        profile_ikb = InlineKeyboardMarkup(row_width=1)

        if not is_blocking_changes:
            profile_ikb.add(self.ib_set_username).add(self.ib_set_fastcup).add(self.ib_set_discord)

        profile_ikb.add(self.ib_back_to_menu)

        return profile_ikb
