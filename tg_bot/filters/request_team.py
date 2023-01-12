from aiogram.dispatcher.filters import BoundFilter


class RequestTeamFilter(BoundFilter):
    key = 'request_team_status'

    def __init__(self, request_team_status=None):
        self.request_team_status = request_team_status

    async def check(self, obj):
        if self.request_team_status is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        team_player = await db_model.get_team_player(user_id=user_id)
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        return self.request_team_status == request_team.request_status
