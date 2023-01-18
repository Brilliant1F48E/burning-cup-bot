from aiogram import Dispatcher

from .confirm_ready import register_handlers_confirm_ready
from .disband import register_handlers_disband
from .invite_code import register_handlers_invite_code
from .kick import register_handlers_kick
from .leave import register_handlers_leave
from .menu import register_handlers_menu
from .set_team_name import register_handlers_set_team_name
from .set_team_photo import register_handlers_set_team_photo
from .create_team import register_handlers_create_team
from .participate import register_handlers_participate
from .composition import register_handlers_team_composition
from .join_team import register_handlers_join_team


def register_handlers_team(dp: Dispatcher):
    register_handlers_leave(dp)
    register_handlers_confirm_ready(dp)
    register_handlers_disband(dp)
    register_handlers_invite_code(dp)
    register_handlers_kick(dp)
    register_handlers_menu(dp)
    register_handlers_participate(dp)
    register_handlers_set_team_name(dp)
    register_handlers_set_team_photo(dp)
    register_handlers_create_team(dp)
    register_handlers_team_composition(dp)
    register_handlers_join_team(dp)
