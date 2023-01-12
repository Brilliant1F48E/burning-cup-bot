from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.keyboards.base_kb import BaseKb

from tg_bot.misc.emoji import Emoji
from tg_bot.types.request import RequestStatus
from tg_bot.types.registration import RegistrationStatus


class TeamKb(BaseKb):
    ib_create_team = InlineKeyboardButton("👥 Создать команду", callback_data="create_team")
    ib_join_team = InlineKeyboardButton("Присоединиться к команде", callback_data="join_team")

    ib_leave_from_team = InlineKeyboardButton("Покинуть команду", callback_data="leave_from_team")
    ib_confirm_ready = InlineKeyboardButton(f"{Emoji.burn} Подтвердить готовность", callback_data="confirm_ready")

    ib_kick_from_team = InlineKeyboardButton("Выгнать", callback_data="kick_from_team")
    ib_participate = InlineKeyboardButton(f"{Emoji.burn} Принять участие", callback_data="participate")
    ib_disbanded_team = InlineKeyboardButton(f"Расформировать", callback_data="disband_team")

    ib_team_composition = InlineKeyboardButton("Состав команды", callback_data="team_composition")
    ib_invite_code = InlineKeyboardButton("Код приглашения", callback_data="invite_code")
    ib_set_team_name = InlineKeyboardButton("Изменить название", callback_data="set_team_name")
    ib_set_team_photo = InlineKeyboardButton("Изменить фото", callback_data="set_team_photo")

    async def get_team_ikb(self, team_exist: bool = False, is_captain: bool = False, is_ready: bool = False, registration=None,
                           request_team=None):
        team_ikb = InlineKeyboardMarkup(row_width=1)

        if not team_exist:
            team_ikb.add(self.ib_create_team).add(self.ib_join_team).add(self.ib_back_to_menu)

            return team_ikb

        team_ikb.add(self.ib_team_composition)

        if is_captain:
            team_ikb.add(self.ib_disbanded_team).add(self.ib_set_team_name).add(self.ib_set_team_photo).add(self.ib_invite_code)
            if registration:
                print(registration.registration_status)
                if registration.registration_status == RegistrationStatus.OPEN:
                    if request_team is None:
                        team_ikb.add(self.ib_participate)
                    elif request_team.request_status != RequestStatus.WAIT and request_team.request_status != RequestStatus.PROCESS and request_team.request_status != RequestStatus.SUCCESS:
                        team_ikb.add(self.ib_participate)
        else:
            team_ikb.add(self.ib_leave_from_team)

        if not is_ready:
            team_ikb.add(self.ib_confirm_ready)

        team_ikb.add(self.ib_back_to_menu)

        return team_ikb

    async def get_team_player_ikb(self, is_captain: bool = False, team_id: int = None, is_tool_park: bool = None,
                                  is_participate: bool = False) -> InlineKeyboardMarkup:
        team_ikb = InlineKeyboardMarkup(row_width=1)

        composition = InlineKeyboardButton('Состав', callback_data='team_composition')
        team_ikb.add(composition)

        if is_tool_park:
            return team_ikb

        if is_captain:
            invite_code = InlineKeyboardButton('Код приглашения', callback_data=f'team_invite_code?team_id={team_id}')
            disband_team = InlineKeyboardButton('Расформировать команду',
                                                callback_data=f'disband_team?team_id={team_id}')

            team_ikb.add(invite_code).add(disband_team)

        if not is_captain:
            leave_the_team_ib = InlineKeyboardButton('Покинуть команду', callback_data='leave_the_team')

            if not is_participate:
                participate = InlineKeyboardButton('🔥 Принять участие', callback_data='participate')
                team_ikb.add(participate)

            team_ikb.add(leave_the_team_ib)

        team_ikb.add(self.ib_back_to_menu)

        return team_ikb

    async def get_participate_ikb(self) -> InlineKeyboardMarkup:
        participate_ikb = InlineKeyboardMarkup(row_width=1)

        participate_ikb.add(self.ib_participate)

        return participate_ikb

    @staticmethod
    async def get_fail_participate_ikb(team_id: int) -> InlineKeyboardMarkup:
        set_team_ikb = InlineKeyboardMarkup(row_width=1)

        ib_repeated_request = InlineKeyboardButton('Повторная заявка', callback_data='participate')
        ib_set_team_name = InlineKeyboardButton('Изменить название', callback_data=f'set_team_name?team_id={team_id}')
        ib_set_team_photo = InlineKeyboardButton('Изменить фото', callback_data=f'set_team_photo?team_id={team_id}')
        set_team_ikb.add(ib_set_team_name).add(ib_set_team_photo).add(ib_repeated_request)

        return set_team_ikb

    @staticmethod
    async def get_confirm_participate_ikb() -> InlineKeyboardMarkup:
        participate_ikb = InlineKeyboardMarkup(row_width=2)

        yes = InlineKeyboardButton('Да', callback_data='confirm_participate')
        no = InlineKeyboardButton('Нет', callback_data='back_to_team')

        participate_ikb.insert(yes).insert(no)

        return participate_ikb

    @staticmethod
    async def get_confirm_kick_team_player_ikb(player_id: int) -> InlineKeyboardMarkup:
        confirm_kick_team_player_ikb = InlineKeyboardMarkup(row_width=2)

        yes = InlineKeyboardButton('Да', callback_data=f'confirm_kick_team_player?player_id={player_id}')
        no = InlineKeyboardButton('Нет', callback_data=f'team_composition')

        confirm_kick_team_player_ikb.add(yes).insert(no)

        return confirm_kick_team_player_ikb

    @staticmethod
    async def get_confirm_leave_the_team_ikb() -> InlineKeyboardMarkup:
        confirm_leave_the_team = InlineKeyboardMarkup(row_width=2)

        ib_yes_confirm_leave_the_team = InlineKeyboardButton('Да',
                                                             callback_data=f'confirm_leave_the_team')
        ib_no_confirm_leave_the_team = InlineKeyboardButton('Нет', callback_data=f'back_to_team')

        confirm_leave_the_team.add(ib_yes_confirm_leave_the_team).insert(ib_no_confirm_leave_the_team)
        return confirm_leave_the_team

    @staticmethod
    async def get_confirm_disband_team(team_id: int) -> InlineKeyboardMarkup:
        confirm_disband_team = InlineKeyboardMarkup(row_width=2)

        ib_yes_confirm_disband_team = InlineKeyboardButton('Да',
                                                           callback_data=f'confirm_disband_team?team_id={team_id}')
        ib_no_confirm_disband_team = InlineKeyboardButton('Нет', callback_data=f'back_to_team')

        confirm_disband_team.insert(ib_yes_confirm_disband_team).insert(ib_no_confirm_disband_team)

        return confirm_disband_team

    async def get_generate_invite_code_ikb(self, team_id: int) -> InlineKeyboardMarkup:
        generate_invite_code_ikb = InlineKeyboardMarkup(row_width=1)

        generate_invite_code_ikb.add(
            InlineKeyboardButton('Сгенерировать новый код', callback_data=f'generate_invite_code?team_id={team_id}'))

        generate_invite_code_ikb.add(self.ib_back_to_team)

        return generate_invite_code_ikb

    async def get_team_composition_ikb(self, players: list, captain, is_captain: bool = False,
                                       is_request_team: bool = False) -> InlineKeyboardMarkup:
        team_composition_ikb = InlineKeyboardMarkup(row_width=1)

        captain_ib = InlineKeyboardButton(f'⚜ {captain.username}', url=f'https://t.me/{captain.tg_username}')
        team_composition_ikb.add(captain_ib)

        count_players = len(players)

        for player in players:
            if player is not None:
                status = Emoji.burn if player.get('is_ready') else ''
                team_composition_ikb.add(InlineKeyboardButton(f"{player.get('username')} {status}",
                                                              url=f'https://t.me/{player.get("tg_username")}'))
                if is_captain and not is_request_team:
                    team_composition_ikb.add(
                        InlineKeyboardButton('Кикнуть', callback_data=f'kick_team_player?player_id={player.get("id")}'))

        for i in range(4 - count_players):
            team_composition_ikb.add(InlineKeyboardButton('Пусто', callback_data=' '))

        team_composition_ikb.add(self.ib_back_to_team)
        return team_composition_ikb
