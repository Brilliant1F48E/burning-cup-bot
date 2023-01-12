from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class BaseKb:
    ib_back_to_menu = InlineKeyboardButton('Вернуться', callback_data='back_to_menu')
    ib_back_to_team = InlineKeyboardButton('Назад', callback_data='back_to_team')

    team_endpoint = "team"
    profile_endpoint = "profile"
    rules_endpoint = "rules"
    support_endpoint = "support"

    async def get_back_to_menu_ikb(self) -> InlineKeyboardMarkup:
        back_to_menu_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_menu_ikb.add(self.ib_back_to_menu)

        return back_to_menu_ikb

    async def get_back_to_team_ikb(self) -> InlineKeyboardMarkup:
        back_to_team_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_team_ikb.add(self.ib_back_to_team)

        return back_to_team_ikb
