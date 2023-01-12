from aiogram.dispatcher.filters import BoundFilter


class TournamentFilter(BoundFilter):
    key = 'is_tournament'

    def __init__(self, is_tournament=None):
        self.is_tournament = is_tournament

    async def check(self, obj):
        if self.is_tournament is None:
            return False

        db_model = obj.bot.get('db_model')

        is_tournament = await db_model.is_tournament()
        return self.is_tournament == is_tournament
