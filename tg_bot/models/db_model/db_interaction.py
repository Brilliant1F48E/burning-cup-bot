import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_

from tg_bot.models.db_model.models import UserTG, Team, RequestMember, Member, Moderator, Player, TeamPlayer, \
    TeamStatus, Institution, RequestTeam, TournamentTeam, Registration, Match, Game, Day, Tournament
from tg_bot.models.db_model.db_client import DBClient

from tg_bot.types.moderator import ModeratorRule
from tg_bot.types.team_player import TeamPlayerStatus
from tg_bot.types.request import RequestStatus
from tg_bot.types.match import MatchStatus
from tg_bot.types.game import GameStatus
from tg_bot.types.tournament import TournamentStatus
from tg_bot.types.registration import RegistrationStatus
from tg_bot.types.days import DayStatus


class DBInteraction(DBClient):
    def __init__(self, sqlalchemy_url: str, base):
        super().__init__(sqlalchemy_url, base)
        self.connect = sessionmaker(bind=self.engine)
        self.session = self.connect()

    # RequestsTeam
    async def add_request_team(self, team_id: int):
        self.session.add(RequestTeam(
            team_id=team_id
        ))
        self.session.commit()

    async def set_request_team_comment(self, request_team_id: int, comment: str):
        self.session.query(RequestTeam).filter(RequestTeam.id == request_team_id).update({'comment': comment})
        self.session.commit()

    async def get_request_team_by_team_id(self, team_id: int) -> RequestTeam:
        request_team = self.session.query(RequestTeam).filter(RequestTeam.team_id == team_id).order_by(
            RequestTeam.id.desc()
        ).first()

        return request_team

    async def set_request_team_status(self, request_team_id: int, request_status: str) -> None:
        self.session.query(RequestTeam).filter(RequestTeam.id == request_team_id).update({
            "request_status": request_status
        })
        self.session.commit()

    async def get_request_team(self, request_team_id: int) -> RequestTeam:
        request_team = self.session.query(RequestTeam).filter(RequestTeam.id == request_team_id).first()

        return request_team

    async def get_team_requests(self) -> list:
        team_requests = self.session.query(RequestTeam).all()

        return team_requests

    async def get_last_user_id(self) -> int:
        user_tg = self.session.query(UserTG).order_by(UserTG.id.desc()).first()

        return user_tg.id

    async def add_institution(self, name: str, institution_type: str) -> None:
        self.session.add(Institution(
            name=name,
            institution_type=institution_type
        ))
        self.session.commit()

    async def get_institutions(self, institution_type):
        institutions = self.session.query(Institution).filter(
            Institution.institution_type == institution_type).all()

        return institutions

    async def get_institution(self, institution_id: int, institution_type: str) -> Institution:
        institution = self.session.query(Institution).filter(
            and_(Institution.id == institution_id, Institution.institution_type == institution_type)).first()

        return institution

    async def is_user(self, user_id: int) -> bool:
        users = self.session.query(UserTG).filter(UserTG.id == user_id).all()
        user_exist = bool(len(users))

        return user_exist

    async def add_user(self, user_id: int, username):

        user = UserTG(
            id=user_id,
            username=username
        )

        self.session.add(user)
        self.session.commit()

        return user

    async def get_users(self):

        users = self.session.query(UserTG).all()

        return users

    async def moderator_exist(self, user_id: int) -> bool:

        moderator = self.session.query(Moderator).filter(Moderator.user_id == user_id).all()

        return bool(len(moderator))

    async def add_moderator(self, user_id: int, rule: str):

        moderator = Moderator(
            user_id=user_id,
            rule=rule
        )
        self.session.add(moderator)
        self.session.commit()

    async def get_moderators(self, rule: str):

        moderators = self.session.query(Moderator).filter(
            or_(Moderator.moderator_rule == rule, Moderator.moderator_rule == ModeratorRule.ALL)).all()

        return moderators

    async def request_member_exist(self, user_id: int) -> bool:

        requests_member = self.session.query(RequestMember).filter(RequestMember.user_id == user_id).all()
        request_member_exist = bool(len(requests_member))

        return request_member_exist

    async def add_request_member(self, user_id: int, last_name: str, first_name: str, patronymic: str,
                                 document_photo: str, group: str, institution: str,
                                 member_type: str):
        request_member = RequestMember(
            user_id=user_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            document_photo=document_photo,
            group=group,
            institution=institution,
            member_type=member_type
        )

        self.session.add(request_member)
        self.session.commit()

    async def set_request_member_comment(self, request_id: int, comment: str):
        self.session.query(RequestMember).filter(RequestMember.request_id == request_id).update({'comment': comment})
        self.session.commit()

    async def set_request_member_status(self, request_id: int, status: str):
        self.session.query(RequestMember).filter(RequestMember.id == request_id).update(
            {'request_member_status': status})
        self.session.commit()

    async def set_player_status(self, player_id: int, status: str):
        self.session.query(Player).filter(Player.id == player_id).update(
            {'player_status': status})

        self.session.commit()

    async def set_team_player_status(self, team_player_id: int, status: str):
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).order_by(TeamPlayer.id.desc()).update(
            {'team_player_status': status})

        self.session.commit()

    async def set_member_status(self, member_id: int, status: str):
        self.session.query(Member).filter(Member.id == member_id).update(
            {'member_status': status})

        self.session.commit()

    # async def set_team_status(self, team_id: int, status: str):
    #     self.session.query(Member).filter(Member.id == team_id).update(
    #         {'team_status': status})
    #
    #     self.session.commit()

    async def get_request_member(self, request_id: int) -> RequestMember:
        request_member: RequestMember = self.session.query(RequestMember).filter(RequestMember.id == request_id).first()

        return request_member

    async def get_request_member_by_user_id(self, user_id: int) -> RequestMember:
        request_member: RequestMember = self.session.query(RequestMember).filter(RequestMember.user_id == user_id).first()

        return request_member

    async def get_requests_member_by_status(self, status: RequestStatus) -> list:
        requests_member: list = self.session.query(RequestMember).filter(RequestMember.request_member_status == status).all()

        return requests_member

    async def is_member(self, user_id: int) -> bool:
        user = await self.is_user(user_id=user_id)

        if not user:
            return False

        members = self.session.query(Member).filter(Member.user_id == user_id).all()
        is_member = bool(len(members))

        return is_member

    async def add_member(self, user_id: int, last_name: str, first_name: str, patronymic: str,
                         institution: str, member_type: str, group: str):
        self.session.add(Member(
            user_id=user_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            institution=institution,
            group=group,
            member_type=member_type,
        ))
        self.session.commit()

        member = await self.get_member_by_user_id(user_id=user_id)

        return member

    async def get_member(self, member_id: int):
        member = self.session.query(Member).filter(Member.id == member_id).first()

        return member

    async def get_member_by_user_id(self, user_id: int) -> Member:
        member = self.session.query(Member).filter(Member.user_id == user_id).first()

        return member

    async def is_player(self, user_id: int) -> bool:
        if not await self.is_member(user_id=user_id):
            return False

        member = await self.get_member_by_user_id(user_id=user_id)

        players = self.session.query(Player).filter(Player.member_id == member.id).all()
        is_player = bool(len(players))

        return is_player

    async def add_player(self, user_id: int, username: str, tg_username: str, discord: str, fastcup: str):
        member = await self.get_member_by_user_id(user_id=user_id)

        self.session.add(Player(
            member_id=member.id,
            username=username,
            tg_username=tg_username,
            discord=discord,
            fastcup=fastcup
        ))

        self.session.commit()

        player = await self.get_player_by_user_id(user_id=user_id)

        return player

    async def get_player(self, player_id: int) -> Player:
        player = self.session.query(Player).filter(Player.id == player_id).first()

        return player

    async def get_player_by_username(self, username: str) -> Player:
        player = self.session.query(Player).filter(Player.username == username).first()

        return player

    async def get_team_player(self, user_id: int) -> TeamPlayer:
        player: Player = await self.get_player_by_user_id(user_id=user_id)

        team_player: TeamPlayer = await self.get_team_player_by_player_id(player_id=player.id)
        return team_player

    async def get_team_player_by_player_id(self, player_id: int) -> TeamPlayer:
        team_player: TeamPlayer = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player_id).order_by(
            TeamPlayer.id.desc()).first()

        return team_player

    async def get_team_players_by_team_id(self, team_id: int):
        team_players = self.session.query(TeamPlayer).filter(TeamPlayer.team_id == team_id).all()

        return team_players

    async def is_tournament(self):
        tournament = self.session.query(Tournament).filter(and_(Tournament.tournament_status != TournamentStatus.CANCEL,
                                                                Tournament.tournament_status != TournamentStatus.FINISH)).order_by(
            Tournament.id.desc()).first()

        if tournament is None:
            return False

        return True

    async def get_player_by_user_id(self, user_id: int) -> Player:
        member = await self.get_member_by_user_id(user_id=user_id)

        player: Player = self.session.query(Player).filter(Player.member_id == member.id).first()

        return player

    async def set_player_username(self, user_id: int, username: str):
        member = await self.get_member_by_user_id(user_id=user_id)

        self.session.query(Player).filter(Player.member_id == member.id).update({'username': username})

        self.session.commit()

    async def set_player_fastcup(self, user_id: int, fastcup: str):
        member = await self.get_member_by_user_id(user_id=user_id)

        self.session.query(Player).filter(Player.member_id == member.id).update({'fastcup': fastcup})

        self.session.commit()

    async def set_player_discord(self, user_id: int, discord: str):
        member = await self.get_member_by_user_id(user_id=user_id)

        self.session.query(Player).filter(Player.member_id == member.id).update({'username': discord})

        self.session.commit()

    async def get_players(self):
        players = self.session.query(Player).all()

        return players

    async def validation_player_username(self, username: str) -> bool:
        players = self.session.query(Player).filter(Player.username == username).all()

        is_valid_username = bool(len(players))

        return is_valid_username

    async def validation_player_discord(self, discord: str) -> bool:
        players = self.session.query(Player).filter(Player.discord == discord).all()

        is_valid_discord = bool(len(players))

        return is_valid_discord

    async def validation_player_fastcup(self, fastcup: str) -> bool:
        players = self.session.query(Player).filter(Player.fastcup == fastcup).all()

        is_valid_fastcup = bool(len(players))

        return is_valid_fastcup

    async def is_team_player(self, user_id: int) -> bool:
        is_player = await self.is_player(user_id=user_id)

        if not is_player:
            return False

        player = await self.get_player_by_user_id(user_id=user_id)

        team_players = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player.id).all()

        team_player_exist = bool(len(team_players))

        return team_player_exist

    async def add_team_player(self, user_id: int, team_id: int, is_captain: bool = False, is_ready: bool = False) -> Player:
        player = await self.get_player_by_user_id(user_id=user_id)

        team_player = TeamPlayer(
            player_id=player.id,
            team_id=team_id,
            is_captain=is_captain,
            is_ready=is_ready
        )

        self.session.add(team_player)
        self.session.commit()

        return await self.get_team_player_by_user_id(user_id=user_id)

    async def get_team_player_by_user_id(self, user_id: int) -> TeamPlayer:
        player = await self.get_player_by_user_id(user_id=user_id)

        team_player = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player.id).order_by(
            TeamPlayer.id.desc()).first()

        return team_player

    async def get_captain_by_team_id(self, team_id: int) -> TeamPlayer:
        captain = self.session.query(TeamPlayer).filter(
            and_(TeamPlayer.team_id == team_id, TeamPlayer.is_captain)).first()

        return captain

    async def set_team_player_status_by_player_id(self, team_player_id: int, status: str) -> None:
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update({'team_player_status': status})
        self.session.commit()

    async def set_team_player_status(self, team_player_id: int, status: str) -> None:
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update({'team_player_status': status})
        self.session.commit()

    async def set_team_player_participate(self, team_player_id: int, is_participate: bool):
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update(
            {'is_participate': is_participate})
        self.session.commit()

    async def get_team_players(self, team_id: int):
        team_players = self.session.query(TeamPlayer).filter(
            and_(TeamPlayer.team_id == team_id, TeamPlayer.team_player_status == TeamPlayerStatus.ACTIVE)).all()

        return team_players

    async def get_team_players_without_captain(self, team_id: int, captain_id: int):
        team_players = self.session.query(TeamPlayer).filter(
            and_(TeamPlayer.team_id == team_id, TeamPlayer.id != captain_id)).all()

        return team_players

    async def get_team(self, team_id: int) -> Team:
        team = self.session.query(Team).filter(Team.id == team_id).first()

        return team

    async def get_team_by_name(self, name) -> Team:
        team = self.session.query(Team).filter(Team.name == name).first()

        return team

    async def is_valid_invite_code(self, invite_code: str) -> bool:
        invite_codes = self.session.query(Team).filter(
            and_(Team.invite_code == invite_code, Team.team_status == TeamStatus.ACTIVE)).all()

        is_valid_invite_code = bool(len(invite_codes))

        return is_valid_invite_code

    async def set_invite_code(self, team_id: int, invite_code: str):
        self.session.query(Team).filter(Team.id == team_id).update({'invite_code': invite_code})
        self.session.commit()

    async def get_team_by_invite_code(self, invite_code: str) -> Team:
        team = self.session.query(Team).filter(Team.invite_code == invite_code).first()

        return team

    async def get_invite_code(self, team_id):
        team = self.session.query(Team).filter(Team.id == team_id).first()

        return team.invite_code

    async def add_team(self, name: str, photo_telegram_id: str, invite_code: str) -> Team:
        self.session.add(Team(
            name=name,
            photo_telegram_id=photo_telegram_id,
            invite_code=invite_code
        ))
        self.session.commit()

        team = await self.get_team_by_name(name=name)

        return team

    async def get_teams_active(self):
        teams = self.session.query(Team).filter(Team.team_status == TeamStatus.ACTIVE).all()

        return teams

    async def set_team_name(self, team_id: int, name: str):
        self.session.query(Team).filter(Team.id == team_id).update({'name': name})
        self.session.commit()

    async def set_team_photo(self, team_id: int, photo: str):
        self.session.query(Team).filter(Team.id == team_id).update({'photo': photo})
        self.session.commit()
    async def set_team_photo_telegram_id(self, team_id: int, photo_telegram_id: str):
        self.session.query(Team).filter(Team.id == team_id).update({'photo_telegram_id': photo_telegram_id})
        self.session.commit()

    async def set_team_status(self, team_id: int, status: str):
        self.session.query(Team).filter(Team.id == team_id).update({'team_status': status})
        self.session.commit()

    async def get_team_by_id(self, team_id) -> Team:
        team = self.session.query(Team).filter(Team.id == team_id).first()

        return team

    async def is_valid_team_name(self, name: str) -> bool:
        teams = self.session.query(Team).filter(and_(Team.name == name, Team.team_status == TeamStatus.ACTIVE)).all()

        is_valid_team_name = bool(len(teams))
        return is_valid_team_name

    async def add_tournament_team(self, captain_id: int, players: list,
                                  name: str, photo: str):
        self.session.add(TournamentTeam(
            captain_id=captain_id,
            second_player=players[0].player_id,
            third_player=players[1].player_id,
            four_player=players[2].player_id,
            fifth_player=players[3].player_id,
            name=name,
            photo=photo,
        ))
        self.session.commit()

    async def set_tournament_team_group(self, tournament_team_id: int, group: str):
        self.session.query(TournamentTeam).filter(TournamentTeam.id == tournament_team_id).update({'group': group})
        self.session.commit()

    async def get_tournament_team_by_id(self, tournament_team_id: int):
        tournament_team = self.session.query(TournamentTeam).filter(TournamentTeam.id == tournament_team_id).first()

        return tournament_team

    async def get_tournament_teams(self):
        tournament_teams = self.session.query(TournamentTeam).all()

        return tournament_teams

    async def get_tournament_teams_by_group(self, group: str):
        tournament_teams = self.session.query(TournamentTeam).filter(TournamentTeam.group == group).all()

        return tournament_teams

    async def get_all_team_players(self):
        team_players = self.session.query(TeamPlayer).all()

        return team_players

    async def add_registration(self, opening_date: datetime, tournament_id: int) -> Registration:
        self.session.add(Registration(
            tournament_id=tournament_id,
            opening_date=opening_date,
        ))

        self.session.commit()

        registration = await self.get_registration(tournament_id=tournament_id)

        return registration

    async def get_registration(self, tournament_id: int) -> Registration:
        registration = self.session.query(Registration).filter(Registration.tournament_id == tournament_id).order_by(
            Registration.id.desc()).first()

        return registration

    async def set_registration_status(self, registration_id: int, status: str):
        self.session.query(Registration).filter(Registration.id == registration_id).update(
            {'registration_status': status})
        self.session.commit()

    async def set_data_close_registration(self, registration_id: int, closing_date: float):
        self.session.query(Registration).filter(Registration.id == registration_id).update(
            {'closing_date': closing_date})

    async def add_match(self, number_match: int, stage: str, group: str = None, next_number_match: int = None,
                        first_tournament_team_id: int = None,
                        second_tournament_team_id: int = None, match_status: str = MatchStatus.WAIT_TEAMS):
        self.session.add(Match(
            number_match=number_match,
            next_number_match=next_number_match,
            stage=stage,
            group=group,
            first_tournament_team_id=first_tournament_team_id,
            second_tournament_team_id=second_tournament_team_id,
            match_status=match_status
        ))

        self.session.commit()

    async def get_matches(self, match_status: str):
        matches = self.session.query(Match).filter(Match.match_status == match_status).all()

        return matches

    async def get_match(self, match_id: int) -> Match:
        match = self.session.query(Match).filter(Match.id == match_id).first()

        return match

    async def set_match_status(self, match_id: int, status: str):
        self.session.query(Match).filter(Match.id == match_id).update({'match_status': status})

        self.session.commit()

    async def add_game(self, match_id: int, start_date: datetime):
        self.session.add(Game(
            match_id=match_id,
            start_date=start_date
        ))
        self.session.commit()

    async def get_game(self, game_id: int):
        games = self.session.query(Game).filter(Game.id == game_id).first()

        return games

    async def get_games(self):
        games = self.session.query(Game).filter(Game.game_status != GameStatus.ONLINE).all()

        return games

    async def update_result_game(self, game_id: int, winner_team_id: int):
        self.session.query(Game).filter(Game.id == game_id).update({'winner_tournament_team_id': winner_team_id})

        self.session.commit()

    async def set_game_status(self, game_id: int, status: str):
        self.session.query(Game).filter(Game.id == game_id).update({'game_status': status})

        self.session.commit()

    async def get_match_by_number_match(self, number_match: int):
        match = self.session.query(Match).filter(Match.number_match == number_match).first()

        return match

    async def match_set_tournament_team(self, team_id: int, position: str, number_match: int):
        self.session.query(Match).filter(Match.number_match == number_match).update({position: team_id})

        self.session.commit()

    async def get_next_game(self):
        game = self.session.query(Game).filter(Game.game_status == GameStatus.WAIT).order_by(
            Game.start_date.desc()).first()

        return game

    async def add_day(self, game_id: int, stream_link: str):
        self.session.add(Day(
            game_id=game_id,
            stream_link=stream_link
        ))

        self.session.commit()

    async def institution_exist(self, name: str):
        institution = self.session.query(Institution).filter(Institution.name == name).first()

        if institution is not None:
            return institution

    async def request_team_exist(self, team_id: int):
        request_team = await self.get_request_team_by_team_id(team_id=team_id)

        return request_team if request_team is not None else None

    async def add_tournament(self, name: str, date_anons: datetime, limit_teams: int,
                             tournament_status: str = TournamentStatus.WAIT):
        self.session.add(Tournament(
            name=name,
            date_anons=date_anons,
            limit_teams=limit_teams,
            tournament_status=tournament_status
        ))
        self.session.commit()

        tournament = await self.get_tournament_by_name(name=name)

        return tournament

    async def get_tournament(self) -> Tournament:
        tournament = self.session.query(Tournament).filter(
            Tournament.tournament_status != TournamentStatus.FINISH).order_by(Tournament.id.desc()).first()

        return tournament

    async def set_tournament(self, tournament_id: int, limit_teams: int = None, anons_date: datetime = None,
                             tournament_status: str = None):
        update = {}

        if limit_teams:
            update = {'limit_teams': limit_teams}
        elif anons_date:
            update = {'anons_date': anons_date}
        elif tournament_status:
            update = {'anons_date': tournament_status}

        self.session.query(Tournament).filter(Tournament.id == tournament_id).update(update)

    async def get_tournament_by_name(self, name: str):
        tournament = self.session.query(Tournament).filter(Tournament.name == name).order_by(
            Tournament.id.desc()).first()

        return tournament

    async def is_registration(self) -> bool:
        if not await self.is_tournament():
            return False

        is_registration = self.session.query(Registration).filter(
            and_(Registration.registration_status != RegistrationStatus.CLOSE,
                 Registration.registration_status != RegistrationStatus.CANCEL)).order_by(
            Registration.id.desc()).first()

        if is_registration is None:
            return False

        return True

    async def get_day(self) -> Day:
        day = self.session.query(Day).filter(Day.day_status == DayStatus.ACTIVE).order_by(Day.id.desc()).first()

        return day

    async def set_day_status(self, day_id: int, status: str):
        self.session.query(Day).filter(Day.id == day_id).update({'day_status': status})

        self.session.commit()

    async def get_teams(self):
        teams = self.session.query(Team).all()

        return teams

    async def set_is_captain(self, team_player_id: int, is_captain: bool):
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update({
            "is_captain": is_captain
        })

        self.session.commit()

    async def set_team_player_is_ready(self, team_player_id: int, is_ready: bool) -> None:
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update({
            "is_ready": is_ready
        })

        self.session.commit()

    async def set_registration_closing_date(self, registration_id: int, closing_date: datetime):
        self.session.query(Registration).filter(Registration.id == registration_id).update({
            "closing_date": closing_date
        })

        self.session.commit()

    async def get_member_requests(self):
        member_requests = self.session.query(RequestMember).all()

        return member_requests

