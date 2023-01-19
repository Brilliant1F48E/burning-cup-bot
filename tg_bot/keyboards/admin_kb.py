from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.types.registration import RegistrationStatus
from tg_bot.types.tournament import TournamentStatus
from tg_bot.models.db_model.models import Player


class AdminKb:
    #
    ib_spam = InlineKeyboardButton("Рассылка", callback_data="spam")

    # Back
    ib_back_to_menu = InlineKeyboardButton("Вернуться", callback_data="back_to_menu")
    ib_back_to_tournament = InlineKeyboardButton("Вернуться", callback_data="back_to_tournament")
    ib_back_to_registration = InlineKeyboardButton("Вернуться", callback_data="back_to_registration")

    # Tournament
    ib_set_tournament = InlineKeyboardButton("Назначить", callback_data="set_tournament")

    ib_menu_requests: InlineKeyboardButton = InlineKeyboardButton("Запросы", callback_data="requests?type=member")

    # Days
    ib_days = InlineKeyboardButton("Дни", callback_data="days")

    # Days Actions
    add_day = InlineKeyboardButton("Добавить", callback_data="add_day")
    finish_day = InlineKeyboardButton('Закончить', callback_data='finish_day')
    delete_day = InlineKeyboardButton('Удалить', callback_data='delete_day')
    set_day = InlineKeyboardButton('Изменить', callback_data='set_day')

    # Games
    ib_games = InlineKeyboardButton("Игры", callback_data="games")

    # Matches
    ib_matches = InlineKeyboardButton("Матчи", callback_data="matches")

    # Registration
    ib_registration = InlineKeyboardButton("Регистрация", callback_data="registration")

    ib_team_requests = InlineKeyboardButton("Запросы", callback_data="requests?type=team")

    ib_view_all_team_requests = InlineKeyboardButton("Все", callback_data="get_all")

    # Registration Actions
    ib_set_registration = InlineKeyboardButton("Назначить", callback_data="set_registration")
    ib_cancel_registration = InlineKeyboardButton("Отменить", callback_data="cancel_registration")
    ib_view_registration = InlineKeyboardButton("Посмотреть", callback_data="view_registration")

    # Tournament Teams
    ib_tournament_teams = InlineKeyboardButton("Турнирные команды", callback_data="tournament_teams")

    # Players
    ib_players = InlineKeyboardButton("Игроки", callback_data="players")

    ib_view_all_players = InlineKeyboardButton("Показать всех", callback_data="view_all_players")

    # Member Requests
    ib_member_requests = InlineKeyboardButton("Участники", callback_data="member_requests")
    ib_view_all_member_requests = InlineKeyboardButton("Все", callback_data="view_member_requests")
    ib_view_member_requests = InlineKeyboardButton("Показать", callback_data="view_member_request")

    # Tournament team Requests
    ib_tournament_team_requests = InlineKeyboardButton("Турнирные команды", callback_data="tournament_team_requests")
    ib_view_all_tournament_team_requests = InlineKeyboardButton("Все", callback_data="view_all_tournament_team_requests")

    # Search
    ib_search_player = InlineKeyboardButton("Поиск", callback_data="search_player_select")
    ib_search_player_by_user_id = InlineKeyboardButton("По user_id", callback_data="search_player?by=user_id")
    ib_search_player_by_username = InlineKeyboardButton("По username", callback_data="search_player?by=username")
    ib_search_player_by_tg_username = InlineKeyboardButton("По tg_username", callback_data="search_player?by=tg_username")

    # Teams
    ib_teams = InlineKeyboardButton("Игроки", callback_data="teams")

    ib_view_all_teams = InlineKeyboardButton("Показать всех", callback_data="view_all_teams")

    # Search
    ib_search_team = InlineKeyboardButton("Поиск", callback_data="search_team_select")
    ib_search_team_by_user_id = InlineKeyboardButton("По названию", callback_data="search_team?by=name")

    def __init__(self):
        self.tournament_teams = InlineKeyboardButton('Турнирые команды', callback_data='tournament_teams')

        self.registration = InlineKeyboardButton('Регистрация', callback_data='registration')

        self.days = InlineKeyboardButton('Дни', callback_data='days')
        self.back_to_days = InlineKeyboardButton('Вернуться', callback_data='back_to_days')

        self.games = InlineKeyboardButton('Игры', callback_data='games')
        self.matches = InlineKeyboardButton('Матчи', callback_data='matches')
        self.maps = InlineKeyboardButton('Карты', callback_data='maps')

        self.tournaments = InlineKeyboardButton('Турниры', callback_data='tournaments')
        self.players = InlineKeyboardButton('Игроки', callback_data='player')
        self.team_players = InlineKeyboardButton('Командные игроки', callback_data='team_players')
        self.users = InlineKeyboardButton('Пользователи', callback_data='preplayer')
        self.teams = InlineKeyboardButton('Команды', callback_data='teams')

        self.add_match = InlineKeyboardButton('Добавить матч', callback_data='add_match')
        self.get_matches = InlineKeyboardButton('Получить матчи', callback_data='get_matches')
        self.set_match = InlineKeyboardButton('Изменить матч', callback_data='set_match')

        self.open_registration = InlineKeyboardButton('Назначить регистрацию', callback_data='open_registration')
        self.set_registration = InlineKeyboardButton('Изменить регистрацию', callback_data='set_registration')
        self.cancel_registration = InlineKeyboardButton('Отменить регистрацию', callback_data='cancel_registration')
        self.view_registration_conf = InlineKeyboardButton('Посмотреть регистрацию', callback_data='view_registration')

        self.back_to_registration = InlineKeyboardButton('Вернуться', callback_data='back_to_registration')

        self.view_tournament_teams = InlineKeyboardButton('Показать команды', callback_data='view_teams')
        self.block_team = InlineKeyboardButton('Заблокировать команду', callback_data='block_team')

        self.set_anons_date = InlineKeyboardButton('Дату анонса', callback_data='set_date_anons')
        self.set_limit_teams = InlineKeyboardButton('Ограничение команд', callback_data='set_limit_teams')
        self.set_tournament_status = InlineKeyboardButton('Статус', callback_data='set_tournament_status')

    async def get_team_requests_ikb(self) -> InlineKeyboardMarkup:
        team_requests_ikb = InlineKeyboardMarkup(row_width=2)

        team_requests_ikb.add(self.ib_view_all_team_requests)

        return team_requests_ikb

    async def get_moderation_request_team_ikb(self, request_team_id: int) -> InlineKeyboardMarkup:
        moderation_request_team_ikb = InlineKeyboardMarkup(row_width=2)

        ib_valid = InlineKeyboardButton("Ок", callback_data=f"moderation_request_team?result=SUCCESS&request_team_id={request_team_id}")
        ib_no_valid = InlineKeyboardButton("Нет", callback_data=f"moderation_request_team?result=FAIL&request_team_id={request_team_id}")
        ib_set_request_team_status = InlineKeyboardButton("Изменить статус", callback_data=f"set_request_team_status?request_team_id={request_team_id}")

        moderation_request_team_ikb.add(ib_valid).add(ib_no_valid).add(ib_set_request_team_status)

        return moderation_request_team_ikb

    async def get_view_all_team_requests_ikb(self, team_requests: list) -> InlineKeyboardMarkup:
        view_all_team_requests_ikb = InlineKeyboardMarkup(row_width=1)

        for team_request in team_requests:
            view_all_team_requests_ikb.add(InlineKeyboardButton(
                text=f"{team_request.request_status} {team_request.date_request}", callback_data=f"view_team_request?team_request_id={team_request.id}"
            ))

        return view_all_team_requests_ikb

    async def get_menu_requests_ikb(self) -> InlineKeyboardMarkup:
        menu_requests_ikb = InlineKeyboardMarkup(row_width=1)

        menu_requests_ikb.add(self.ib_member_requests)

        return menu_requests_ikb

    async def get_member_requests_ikb(self) -> InlineKeyboardMarkup:
        member_requests_ikb = InlineKeyboardMarkup(row_width=1)

        member_requests_ikb.add(self.ib_view_all_member_requests)

        return member_requests_ikb

    async def get_view_member_requests_ikb(self, member_requests: list) -> InlineKeyboardMarkup:
        view_member_requests = InlineKeyboardMarkup(row_width=1)

        for member_request in member_requests:
            view_member_requests.add(InlineKeyboardButton(
                f"{member_request.request_member_status} {member_request.last_name} {member_request.first_name} {member_request.patronymic} {member_request.group}", callback_data=" "
            ))
            view_member_requests.add(InlineKeyboardButton(
                "Показать", callback_data=f"view_request_member?user_id={member_request.user_id}"
            ))

        return view_member_requests

    async def get_start_ikb(self) -> InlineKeyboardMarkup:
        start_ikb = InlineKeyboardMarkup(row_width=1)

        start_buttons = [
            self.ib_spam,
            self.tournaments,
            self.teams,
            self.players,
            self.ib_menu_requests
        ]

        start_ikb.add(*start_buttons)

        return start_ikb

    async def get_tournament_ikb(self, tournament=None, registration=None) -> InlineKeyboardMarkup:
        tournament_ikb = InlineKeyboardMarkup(row_width=1)

        if not tournament or tournament.tournament_status == TournamentStatus.CANCEL or tournament.tournament_status == TournamentStatus.FINISH:
            tournament_ikb.add(self.ib_set_tournament)
        elif not registration or registration.registration_status == RegistrationStatus.CANCEL:
            tournament_ikb.add(self.ib_registration)
        elif registration.registration_status == RegistrationStatus.CLOSE:
            tournament_ikb.add(self.ib_registration).add(self.tournament_teams).add(self.matches).add(self.games).add(self.days)
        elif registration.registration_status != RegistrationStatus.CANCEL:
            tournament_ikb.add(self.ib_registration).add(self.tournament_teams)

        tournament_ikb.add(self.ib_back_to_menu)

        return tournament_ikb

    async def get_registration_ikb(self, registration=None) -> InlineKeyboardMarkup:
        registration_ikb = InlineKeyboardMarkup(row_width=1)

        if not registration or registration.registration_status == RegistrationStatus.CANCEL:
            registration_ikb.add(self.ib_set_registration)
        elif registration.registration_status == RegistrationStatus.OPEN:
            registration_ikb.add(self.ib_cancel_registration).add(self.ib_view_registration).add(self.ib_team_requests)
        elif registration.registration_status == RegistrationStatus.CLOSE:
            registration_ikb.add(self.ib_view_registration).add(self.ib_team_requests)

        registration_ikb.add(self.ib_back_to_tournament)

        return registration_ikb

    async def get_players_ikb(self, is_players: bool = False) -> InlineKeyboardMarkup:
        players_ikb = InlineKeyboardMarkup(row_width=1)

        if is_players:
            players_ikb.add(self.ib_search_player).add(self.ib_view_all_players)

        players_ikb.add(self.ib_back_to_tournament)

        return players_ikb

    async def get_teams_ikb(self, is_teams: bool = False) -> InlineKeyboardMarkup:
        teams_ikb = InlineKeyboardMarkup(row_width=1)

        if is_teams:
            teams_ikb.add(self.ib_search_team).add(self.ib_view_all_teams)

        teams_ikb.add(self.ib_back_to_tournament)

        return teams_ikb

    async def get_menu_view_all_players(self, players: list) -> InlineKeyboardMarkup:
        menu_view_all_players = InlineKeyboardMarkup(row_width=1)

        for player in players:
            menu_view_all_players.add(
                InlineKeyboardButton(text=player.username, callback_data=f'view_player?player_id={player.id}')
            )

        return menu_view_all_players

    async def get_menu_players_ikb(self, players: list) -> InlineKeyboardMarkup:
        menu_players_ikb = InlineKeyboardMarkup(row_width=1)

        for player in players:
            menu_players_ikb.add(
                InlineKeyboardButton(text=player.username, callback_data=f'view_player?player_id={player.id}')
            )

        return menu_players_ikb

    async def get_menu_teams_ikb(self, teams: list) -> InlineKeyboardMarkup:
        menu_teams_ikb = InlineKeyboardMarkup(row_width=1)

        for team in teams:
            menu_teams_ikb.add(
                InlineKeyboardButton(team.name, callback_data=f'view_team?team_id={team.id}')
            )

        return menu_teams_ikb

    async def get_view_team_ikb(self, players: list, captain, team_id: int) -> InlineKeyboardMarkup:
        view_team_ikb = InlineKeyboardMarkup(row_width=1)

        view_team_ikb.add(InlineKeyboardButton(
            f"⚜ {captain.username}", url=f"https://t.me/{captain.tg_username}"
        ))
        view_team_ikb.add(InlineKeyboardButton(
            f"Игрок", callback_data=f"view_player?player_id={captain.id}"
        ))

        if players:
            for player in players:
                view_team_ikb.add(InlineKeyboardButton(
                    f"{player.username}", url=f"https://t.me/{player.tg_username}"
                ))
                view_team_ikb.add(InlineKeyboardButton(
                    f"Игрок", callback_data=f"view_player?player_id={player.id}"
                ))

            if len(players) != 4:
                for empty in range(4 - len(players)):
                    view_team_ikb.add(InlineKeyboardButton(
                        f"", callback_data=" "
                    ))

        view_team_ikb.add(InlineKeyboardButton(
            "Забанить", callback_data=f"banned_team?team_id={team_id}"
        ))
        view_team_ikb.add(InlineKeyboardButton(
            "Разбанить", callback_data=f"unbanned_team?team_id={team_id}"
        ))
        return view_team_ikb

    async def get_set_tournament_ikb(self) -> InlineKeyboardMarkup:
        set_tournament_ikb = InlineKeyboardMarkup(row_width=1)

        set_tournament_ikb.add(self.set_anons_date).add(self.set_limit_teams).add(self.set_tournament_status)

        return set_tournament_ikb

    async def get_menu_tournament_teams_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        menu_tournament_teams_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            menu_tournament_teams_ikb.add(InlineKeyboardButton(
                text=tournament_team.name, callback_data=f'view_tournament_team?tournament_team_id={tournament_team.id}'
            ))

        return menu_tournament_teams_ikb

    async def get_menu_tournament_management_ikb(self, registration) -> InlineKeyboardMarkup:
        menu_tournaments_ikb = InlineKeyboardMarkup(row_width=1)

        menu_tournaments_ikb.add(self.registration)

        if registration:
            if registration.registration_status != RegistrationStatus.WAIT:
                menu_tournaments_ikb.add(self.tournament_teams)

            if registration.registration_status == RegistrationStatus.CLOSE:
                menu_tournaments_ikb.add(self.days).add(self.games).add(self.matches)

        return menu_tournaments_ikb

    async def get_menu_tournaments_ikb(self, is_tournament: bool) -> InlineKeyboardMarkup:
        menu_tournaments_ikb = InlineKeyboardMarkup(row_width=1)

        if is_tournament:
            menu_tournaments_ikb.add(InlineKeyboardButton(
                'Управление', callback_data='tournament_management'
            ))
        else:
            menu_tournaments_ikb.add(InlineKeyboardButton(
                'Назначить турнир', callback_data='add_tournament'
            ))

        return menu_tournaments_ikb

    async def get_add_day_choice_game_ikb(self, game) -> InlineKeyboardMarkup:
        add_day_choice_game_ikb = InlineKeyboardMarkup(row_width=1)

        add_day_choice_game_ikb.add(
            InlineKeyboardButton(f'{game.get("first_tournament_team").name} vs {game.get("second_tournament_team").name}', callback_data=f'add_day_choice_game?game_id={game.get("id")}')
        )
        return add_day_choice_game_ikb

    async def get_confirm_finish_day_ikb(self) -> InlineKeyboardMarkup:
        menu_confirm_finish_day_ikb = InlineKeyboardMarkup(row_width=1)

        button_answer_yes = InlineKeyboardButton(text='Да', callback_data='confirm_finish_day')
        button_answer_no = InlineKeyboardButton(text='Нет', callback_data='back_to_days')

        menu_confirm_finish_day_ikb.add(button_answer_yes).add(button_answer_no)

        return menu_confirm_finish_day_ikb

    async def get_menu_days_ikb(self, day) -> InlineKeyboardMarkup:
        menu_days_ikb = InlineKeyboardMarkup(row_width=1)

        if day:
            menu_days_ikb.add(self.delete_day).add(self.set_day).add(self.finish_day)
        else:
            menu_days_ikb.add(self.add_day)

        return menu_days_ikb

    async def get_choice_team_ikb(self, first_team, second_team, game_id: int) -> InlineKeyboardMarkup:
        choice_team_ikb = InlineKeyboardMarkup(row_width=1)

        ib_first_team = InlineKeyboardButton(first_team.name, callback_data=f'choice_team?team_id={first_team.id}&game_id={game_id}')
        ib_second_team = InlineKeyboardButton(second_team.name, callback_data=f'choice_team?team_id={second_team.id}&game_id={game_id}')

        choice_team_ikb.add(ib_first_team).add(ib_second_team)

        return choice_team_ikb

    async def get_choice_game_ikb(self, games: list) -> InlineKeyboardMarkup:
        choice_game_ikb = InlineKeyboardMarkup(row_width=1)

        for game in games:
            choice_game_ikb.add(
                InlineKeyboardButton(f'{game.get("first_match_team").name} vs {game.get("second_match_team").name}',
                                     callback_data=f'choice_game?game_id={game.get("id")}&first_team_id={game.get("first_match_team").id}&second_team_id={game.get("second_match_team").id}')
            )

        return choice_game_ikb

    async def get_add_game_ikb(self, matches: list) -> InlineKeyboardMarkup:
        add_game_ikb = InlineKeyboardMarkup(row_width=1)

        for match in matches:
            add_game_ikb.add(
                InlineKeyboardButton(f'{match.get("first_match_team").name} vs {match.get("second_match_team").name}', callback_data=f'choice_match?match_id={match.get("id")}')
            )

        return add_game_ikb

    async def get_games_ikb(self) -> InlineKeyboardMarkup:
        games_ikb = InlineKeyboardMarkup(row_width=1)

        ibs_games_ikb = [
            InlineKeyboardButton('Добавить игру', callback_data='add_game'),
            InlineKeyboardButton('Обновить результаты игры', callback_data='update_result_game'),
        ]

        games_ikb.add(*ibs_games_ikb)

        return games_ikb

    async def get_match_ikb(self) -> InlineKeyboardMarkup:
        match_ikb = InlineKeyboardMarkup(row_width=1)

        ibs_match_ikb = [
            InlineKeyboardButton('Обновить результаты матча', callback_data='add_game')
        ]

    async def get_view_tournament_team_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        view_team_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            view_team_ikb.add(InlineKeyboardButton(
                text=tournament_team.name, callback_data=f'view_tournament_team?tournament_team_id={tournament_team.id}'
            ))

        return view_team_ikb

    async def get_team_ikb(self) -> InlineKeyboardMarkup:
        team_ikb = InlineKeyboardMarkup(row_width=1)

        team_buttons = [
            self.view_tournament_teams,
            self.block_team
        ]

        team_ikb.add(*team_buttons)

        return team_ikb

    async def get_matches_ikb(self) -> InlineKeyboardMarkup:
        matches_ikb = InlineKeyboardMarkup(row_width=1)

        matches_buttons = [
            self.add_match,
            self.set_match,
            self.get_matches
        ]

        matches_ikb.add(*matches_buttons)

        return matches_ikb

    async def get_back_to_registration_ikb(self) -> InlineKeyboardMarkup:
        back_to_registration_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_registration_ikb.add(self.back_to_registration)

        return back_to_registration_ikb

    async def get_view_tournament_teams_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        view_tournament_teams_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            view_tournament_teams_ikb.add(
                InlineKeyboardButton(tournament_team.name, callback_data=f'view_tournament_team?id={tournament_team.id}')
            )

        return view_tournament_teams_ikb
