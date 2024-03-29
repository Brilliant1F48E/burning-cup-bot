from .admin_kb import AdminKb
from .menu_kb import MenuKb
from .profile_kb import ProfileKb
from .register_kb import RegisterKb
from .team_kb import TeamKb
from .moderator_kb import ModeratorKb
from .request import RequestTeamKb, RequestMemberKb

kb = {
    'menu': MenuKb(),
    'admin': AdminKb(),
    'profile': ProfileKb(),
    'register': RegisterKb(),
    'team': TeamKb(),
    'moderator': ModeratorKb(),
    "request": {
        "team": RequestTeamKb(),
        "member": RequestMemberKb(),
    }
}
