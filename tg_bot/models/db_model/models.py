import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, BigInteger, TIMESTAMP

from tg_bot.models.db_model import Base

from tg_bot.types.request.status import RequestStatus
from tg_bot.types.member.status import MemberStatus
from tg_bot.types.player.status import PlayerStatus
from tg_bot.types.team_player.status import TeamPlayerStatus
from tg_bot.types.team.status import TeamStatus
from tg_bot.types.tournament_team import TournamentTeamStatus
from tg_bot.types.registration.status import RegistrationStatus
from tg_bot.types.game.format import FormatGame


class Institution(Base):
    __tablename__ = 'institutions'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True)
    institution_type = Column(String(256), nullable=False)

    def __init__(self, name: str, institution_type: str):
        self.name = name
        self.institution_type = institution_type


class UserTG(Base):
    __tablename__ = 'users_tg'

    id = Column(BigInteger, nullable=False, unique=True, primary_key=True, autoincrement=False)
    username = Column(String(64), nullable=False)


class Moderator(Base):
    __tablename__ = 'moderators'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users_tg.id'), nullable=False)
    moderator_rule = Column(String(32), nullable=False)

    def __init__(self, user_id: int, rule: str):
        self.user_id = user_id
        self.moderator_rule = rule


class RequestMember(Base):
    __tablename__ = 'requests_member'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users_tg.id'), nullable=False)
    date_request = Column(Date, nullable=False)
    last_name = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    patronymic = Column(String(64), nullable=False)
    document_photo = Column(String(256), nullable=False)
    group = Column(String(32), nullable=False)
    institution = Column(String(256), nullable=False)
    member_type = Column(String(64), nullable=False)
    comment = Column(String(256), nullable=True)
    request_member_status = Column(String(64), nullable=False)

    def __init__(self, user_id: int, last_name: str, first_name: str, patronymic: str, document_photo: str,
                 group: str, institution: str, member_type: str):
        self.user_id: int = user_id
        self.date_request: datetime = datetime.datetime.now()
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.patronymic: str = patronymic
        self.document_photo: str = document_photo
        self.group: str = group
        self.institution: str = institution
        self.member_type: str = member_type
        self.request_member_status: str = RequestStatus.WAIT


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users_tg.id'), nullable=False)
    last_name = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    patronymic = Column(String(64), nullable=False)
    institution = Column(String(256), nullable=False)
    group = Column(String(32), nullable=False)
    member_type = Column(String(64), nullable=False)
    member_status = Column(String(64), nullable=False)

    def __init__(self, user_id: int, last_name: str, first_name: str, patronymic: str,
                 institution: str, group: str, member_type: str):
        self.user_id = user_id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.institution = institution
        self.group = group
        self.member_type = member_type
        self.member_status = MemberStatus.ACTIVE


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    tg_username = Column(String(64), nullable=False, unique=True)
    fastcup = Column(String(64), nullable=False, unique=True)
    discord = Column(String(64), nullable=False, unique=True)
    player_status = Column(String(64), nullable=False)

    def __init__(self, member_id: int, username: str, tg_username: str, fastcup: str, discord: str):
        self.member_id = member_id
        self.username = username
        self.tg_username = tg_username
        self.fastcup = fastcup
        self.discord = discord
        self.player_status = PlayerStatus.ACTIVE


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    photo = Column(String(256), nullable=True)
    photo_telegram_id = Column(String(512), nullable=False)
    invite_code = Column(String(256), nullable=False, unique=True)
    team_status = Column(String(64), nullable=False)

    def __init__(self, name: str, photo_telegram_id: str, invite_code: str):
        self.name = name
        self.photo_telegram_id = photo_telegram_id
        self.invite_code = invite_code
        self.team_status = TeamStatus.ACTIVE


class TeamPlayer(Base):
    __tablename__ = 'team_players'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    is_captain = Column(Boolean, nullable=False)
    is_ready = Column(Boolean, nullable=False, default=False)
    team_player_status = Column(String(64), nullable=False)

    def __init__(self, team_id: int, player_id: int, is_captain: bool = False, is_ready: bool = False):
        self.team_id = team_id
        self.player_id = player_id
        self.is_captain = is_captain
        self.is_ready = is_ready
        self.team_player_status = TeamPlayerStatus.ACTIVE


class RequestTeam(Base):
    __tablename__ = 'requests_team'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    date_request = Column(Date, nullable=False)
    comment = Column(String(256), nullable=True, default='')
    request_status = Column(String(64), nullable=False)

    def __init__(self, team_id: int):
        self.team_id: int = team_id
        self.date_request: datetime = datetime.datetime.now()
        self.request_status: str = RequestStatus.WAIT


class TournamentTeam(Base):
    __tablename__ = 'tournament_teams'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    captain_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    second_player = Column(Integer, ForeignKey('players.id'), nullable=False)
    third_player = Column(Integer, ForeignKey('players.id'), nullable=False)
    four_player = Column(Integer, ForeignKey('players.id'), nullable=False)
    fifth_player = Column(Integer, ForeignKey('players.id'), nullable=False)
    group = Column(String(1), nullable=True)
    name = Column(String(64), nullable=False)
    photo = Column(String(256), nullable=False)
    tournament_team_status = Column(String(64), nullable=False)

    def __init__(self, captain_id: int, second_player: int, third_player: int, four_player: int, fifth_player: int,
                 name: str, photo: str):
        self.captain_id: int = captain_id
        self.second_player: int = second_player
        self.third_player: int = third_player
        self.four_player: int = four_player
        self.fifth_player: int = fifth_player
        self.name: str = name
        self.photo: str = photo
        self.tournament_team_status: str = TournamentTeamStatus.ACTIVE


class Tournament(Base):
    __tablename__ = 'tournaments'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    limit_teams = Column(Integer, nullable=False)
    date_anons = Column(TIMESTAMP, nullable=False)
    tournament_status = Column(String(64), nullable=False)

    def __init__(self, name: str, limit_teams: int, date_anons: datetime, tournament_status: str):
        self.name = name
        self.limit_teams = limit_teams
        self.date_anons = date_anons
        self.tournament_status = tournament_status


class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    opening_date = Column(TIMESTAMP, nullable=False)
    closing_date = Column(TIMESTAMP, nullable=True)
    registration_status = Column(String(64), nullable=False)

    def __init__(self, opening_date: datetime, tournament_id: int):
        self.tournament_id = tournament_id
        self.opening_date = opening_date
        self.registration_status = RegistrationStatus.WAIT


class Stage(Base):
    __tablename__ = 'stages'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    first_tournament_team_id = Column(Integer, ForeignKey('tournament_teams.id'), nullable=True)
    second_tournament_team_id = Column(Integer, ForeignKey('tournament_teams.id'), nullable=True)
    next_number_match = Column(Integer, nullable=True)
    number_match = Column(Integer, nullable=False)
    stage = Column(String(64), nullable=False)
    group = Column(String(64), nullable=True)
    format = Column(String(64), nullable=False)
    match_status = Column(String(64), nullable=False)

    def __init__(self, number_match: int, stage: str, match_status: str, format_game: str = FormatGame.BO3,
                 group: str = None, next_number_match: int = None,
                 first_tournament_team_id: int = None, second_tournament_team_id: int = None):
        self.first_tournament_team_id = first_tournament_team_id
        self.second_tournament_team_id = second_tournament_team_id
        self.number_match = number_match
        self.next_number_match = next_number_match
        self.stage = stage
        self.group = group
        self.format = format_game
        self.match_status = match_status


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey('matches.id'), nullable=False)
    winner_tournament_team_id = Column(Integer, ForeignKey('tournament_teams.id'), nullable=True)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=True, unique=True)
    game_status = Column(String(64), nullable=False)

    def __init__(self, match_id: int, start_date: datetime):
        self.match_id = match_id
        self.start_date = start_date
        self.game_status = 'WAIT'


class Day(Base):
    __tablename__ = 'days'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    stream_link = Column(String(256), nullable=False, unique=True)
    date = Column(TIMESTAMP, nullable=True, unique=True)
    day_status = Column(String(64), nullable=False)

    def __init__(self, game_id: int, stream_link: str, day_status: str = 'ONLINE', date: datetime = datetime.datetime.now()):
        self.game_id = game_id
        self.stream_link = stream_link
        self.date = date
        self.day_status = day_status


class Map(Base):
    __tablename__ = 'maps'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    winner_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    name = Column(String(64), nullable=False)
    status_map = Column(String(64), nullable=False)


class MapScore(Base):
    __tablename__ = 'score_matches'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    map_id = Column(Integer, ForeignKey('maps.id'), nullable=False)
    score_first_team = Column(Integer, nullable=False)
    score_second_team = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'preplayer'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
