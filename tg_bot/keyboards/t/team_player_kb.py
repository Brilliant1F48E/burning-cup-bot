from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.misc.emoji import Emoji


class TeamPLayerKb:
    def __init__(self) -> None:
        self.ib_back_to_menu = InlineKeyboardButton('Вернуться', callback_data='back_to_menu')
        self.ib_back_to_team = InlineKeyboardButton(text='Вернуться', callback_data='back_to_team')

        self.ib_participate = InlineKeyboardButton('Принять участие', callback_data='participate')


