from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tg_bot.keyboards.base_kb import BaseKb


class MenuKb(BaseKb):
    def __init__(self):
        super().__init__()
        self.ib_profile = InlineKeyboardButton('👤 Профиль', callback_data='profile')
        self.ib_team = InlineKeyboardButton('👥 Команда', callback_data='team')
        self.ib_rules = InlineKeyboardButton('📝 Регламент', callback_data='rules')
        self.ib_support = InlineKeyboardButton('🆘 Помощь', callback_data='support')

    async def get_menu_ikb(self):
        menu_ikb = InlineKeyboardMarkup(row_width=2)

        menu_ikb.add(self.ib_profile).add(self.ib_team).add(self.ib_rules).add(self.ib_support)

        return menu_ikb
