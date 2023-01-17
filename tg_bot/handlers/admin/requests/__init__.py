from aiogram import Dispatcher

from .enter_comment import register_handlers_enter_comment
from .get import register_handlers_get
from .menu import register_handlers_menu
from .moderation import register_handlers_moderation
from .set_status import register_handlers_set_status
from .view import register_handlers_view


def register_handlers_requests(dp: Dispatcher):
    register_handlers_view(dp)
    register_handlers_enter_comment(dp)
    register_handlers_get(dp)
    register_handlers_menu(dp)
    register_handlers_moderation(dp)
    register_handlers_set_status(dp)
