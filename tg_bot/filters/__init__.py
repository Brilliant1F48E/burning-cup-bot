from aiogram import Dispatcher

from .banned import BannedFilter
from .admin import AdminFilter
from .player import PlayerFilter
from .captain import CaptainFilter
from .member import MemberFilter
from .moderator import ModeratorFilter
from .team_player import TeamPlayerFilter
from .tournament import TournamentFilter
from .request_team import RequestTeamFilter


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(BannedFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(RequestTeamFilter)
    dp.filters_factory.bind(MemberFilter)
    dp.filters_factory.bind(PlayerFilter)
    dp.filters_factory.bind(TeamPlayerFilter)
    dp.filters_factory.bind(CaptainFilter)
    dp.filters_factory.bind(ModeratorFilter)
    dp.filters_factory.bind(TournamentFilter)
