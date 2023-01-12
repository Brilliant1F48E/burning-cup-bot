from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class ModeratorKb:
    # ikb - inline keyboard
    # ib - inline button
    # b - button

    def __init__(self):
        pass

    @staticmethod
    async def get_view_request_team_ikb(team_id: int) -> InlineKeyboardMarkup:
        view_request_team_ikb = InlineKeyboardMarkup(row_width=1)

        view_request_team_ib = InlineKeyboardButton("Верифицировать команду", callback_data=f'view_request_team?request_team_id={team_id}')

        view_request_team_ikb.add(view_request_team_ib)

        return view_request_team_ikb

    @staticmethod
    async def get_verif_request_team_ikb(request_team_id: int) -> InlineKeyboardMarkup:
        verif_request_team_ikb = InlineKeyboardMarkup(row_width=2)

        yes_ib = InlineKeyboardButton('Да', callback_data=f'verif_request_team?request_team_id={request_team_id}&result=yes')
        no_ib = InlineKeyboardButton('Нет', callback_data=f'verif_request_team?request_team_id={request_team_id}&result=no')

        verif_request_team_ikb.insert(yes_ib).insert(no_ib)

        return verif_request_team_ikb

    @staticmethod
    async def get_view_verif_request_ikb(user_id: int) -> InlineKeyboardMarkup:
        verif_request_ikb = InlineKeyboardMarkup(row_width=1)

        ib_viewing_verif_request = InlineKeyboardButton('Просмотреть анкету',
                                                        callback_data=f'view_request_member?user_id={user_id}')

        verif_request_ikb.add(ib_viewing_verif_request)

        return verif_request_ikb

    @staticmethod
    async def get_actions_verif_ikb(user_id: int) -> InlineKeyboardMarkup:
        actions_verif_ikb = InlineKeyboardMarkup(row_width=2)

        ib_action_verif_request_yes = InlineKeyboardButton('✅ Да',
                                                           callback_data=f'verif_request_member?result=yes&user_id={user_id}')
        ib_action_verif_request_no = InlineKeyboardButton('❌ Нет',
                                                          callback_data=f'verif_request_member?result=no&user_id={user_id}')

        actions_verif_ikb.add(ib_action_verif_request_yes).insert(ib_action_verif_request_no)

        return actions_verif_ikb
