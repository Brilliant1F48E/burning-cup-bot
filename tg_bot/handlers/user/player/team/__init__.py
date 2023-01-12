from aiogram import Dispatcher

from .create_team import register_handlers_create_team
from .participate import register_handlers_participate
from .team_handler import register_team_handlers
from .team_composition import register_handlers_team_composition
from .join_team import register_handlers_join_team


def register_handlers_team(dp: Dispatcher):
    register_handlers_participate(dp)
    register_handlers_create_team(dp)
    register_team_handlers(dp)
    register_handlers_team_composition(dp)
    register_handlers_join_team(dp)
