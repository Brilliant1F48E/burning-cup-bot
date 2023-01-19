import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.keyboards import kb
from tg_bot.misc.matches import add_matches
from tg_bot.misc.scripts import notify_user
from tg_bot.types.institution import InstitutionType
from tg_bot.types.moderator import ModeratorRule
from tg_bot.misc.phares import Phrases
from tg_bot.models.db_model.db_interaction import DBInteraction
from tg_bot.models.db_model import Base
from tg_bot.handlers import register_all_handlers


class TgBot:
    def __init__(self, config, schools: list, colleges: list, debug: bool = False):
        self.config = config
        self.debug = debug

        self.schools = schools
        self.colleges = colleges

        self.bot = Bot(token=self.config.tg_bot.token, parse_mode='HTML')

        self.sqlalchemy_database_uri = f'postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}'
        self.db_interaction = DBInteraction(sqlalchemy_url=self.sqlalchemy_database_uri, base=Base)
        self.db_interaction.create_tables()

        self.bot["config"] = self.config
        self.bot["kb"] = kb
        self.bot["phrases"] = Phrases
        self.bot["db_model"] = self.db_interaction
        self.bot["scheduler"] = AsyncIOScheduler(timezone="Asia/Krasnoyarsk")
        self.storage = MemoryStorage()

        self.dp = Dispatcher(self.bot, storage=self.storage)

        logging.basicConfig(
            level=logging.INFO,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        )
        self.logger = logging.getLogger(__name__)

    async def run(self, register_all_filters=None):
        self.logger.info("Starting bot")

        await self.add_admin_data()
        await self.add_institutions()

        if register_all_filters:
            register_all_filters(self.dp)

        register_all_handlers(self.dp)

        try:
            await self.dp.start_polling()
        finally:
            await self.dp.storage.close()
            await self.dp.storage.wait_closed()
            await self.bot.session.close()

    async def add_admin_data(self):
        admin_id = self.config.tg_bot.admin_id

        if not await self.db_interaction.is_user(user_id=admin_id):
            await self.db_interaction.add_user(user_id=admin_id, username='lxrd1995')

        if not await self.db_interaction.moderator_exist(user_id=admin_id):
            await self.db_interaction.add_moderator(user_id=admin_id, rule=ModeratorRule.ALL)

    async def add_institutions(self):
        for school in self.schools:
            if not await self.db_interaction.institution_exist(name=school):
                await self.db_interaction.add_institution(name=school, institution_type=InstitutionType.SCHOOL)

        for college in self.colleges:
            if not await self.db_interaction.institution_exist(name=college):
                await self.db_interaction.add_institution(name=college, institution_type=InstitutionType.COLLEGE)

    async def add_test_account(self):
        username = "moon"
        user_id = 5317213391

        user = await self.db_interaction.add_user(user_id=user_id, username=username)

        await self.db_interaction.add_member(
            user_id=user.id,
            first_name="Константин",
            last_name="Константинов",
            patronymic="Константинович",
            group="Д192/2",
            institution="СПК",
            member_type="STUDENT",
        )

        await self.db_interaction.add_player(
            user_id=user.id,
            username=username,
            discord=username + "#",
            fastcup=username,
            tg_username=username
        )

        await self.db_interaction.add_team_player(
            user_id=user.id,
            team_id=1,
            is_captain=True,
        )

    async def add_test_team(self):
        team_name = "moon"
        invite_code = "231"
        photo_telegram_id = "AgACAgIAAxkBAAIBOGOZ2GV1BPoJddgFuzrVf1OmzjQ4AAJvxjEbNybQSHWUiqZXfA5oAQADAgADeQADLAQ"

        team = await self.db_interaction.add_team(
            name=team_name,
            photo="SkyTeam.png",
            photo_telegram_id=photo_telegram_id,
            invite_code=invite_code
        )

        username = "moon_player"
        for k in range(0, 4, 1):
            last_user_id = await self.db_interaction.get_last_user_id()
            user_id = last_user_id + 1
            tmp_username = username + str(user_id)

            user = await self.db_interaction.add_user(user_id=user_id, username=tmp_username)

            await self.db_interaction.add_member(
                user_id=user.id,
                first_name="Константин",
                last_name="Константинов",
                patronymic="Константинович",
                group="Д192/2",
                institution="СПК",
                member_type="STUDENT",
            )

            await self.db_interaction.add_player(
                user_id=user.id,
                username=tmp_username,
                discord=tmp_username + "#",
                fastcup=tmp_username,
                tg_username=tmp_username
            )

            await self.db_interaction.add_team_player(
                user_id=user.id,
                team_id=team.id,
                is_captain=False,
                is_ready=True
            )

    async def add_test_tournament_team(self, count_teams: int):
        team_name = "test_team"
        invite_code = "12345435346235"
        photo_telegram_id = "23412345667547"

        for i in range(0, count_teams, 1):
            tmp_team_name = team_name + str(i)
            tmp_invite_code = invite_code + str(i)
            tmp_photo_telegram_id = photo_telegram_id + str(i)

            team = await self.db_interaction.add_team(
                name=tmp_team_name,
                photo="SkyTeam.png",
                photo_telegram_id=tmp_photo_telegram_id,
                invite_code=tmp_invite_code
            )

            captain = ""
            players = []

            username = "test"
            for k in range(0, 5, 1):
                last_user_id = await self.db_interaction.get_last_user_id()
                user_id = last_user_id + 1
                tmp_username = username + str(user_id)

                user = await self.db_interaction.add_user(user_id=user_id, username=tmp_username)

                await self.db_interaction.add_member(
                    user_id=user.id,
                    first_name="Константин",
                    last_name="Константинов",
                    patronymic="Константинович",
                    group="Д192/2",
                    institution="СПК",
                    member_type="STUDENT",
                )

                if k == 4:
                    await self.db_interaction.add_player(
                        user_id=user.id,
                        username=tmp_username,
                        discord=tmp_username + "#",
                        fastcup=tmp_username,
                        tg_username=tmp_username
                    )
                    captain = await self.db_interaction.add_team_player(
                        user_id=user.id,
                        team_id=team.id,
                        is_captain=True,
                        is_ready=True
                    )
                else:
                    await self.db_interaction.add_player(
                        user_id=user.id,
                        username=tmp_username,
                        discord=tmp_username + "#",
                        fastcup=tmp_username,
                        tg_username=tmp_username
                    )

                    players.append(
                        await self.db_interaction.add_team_player(
                            user_id=user.id,
                            team_id=team.id,
                            is_captain=False,
                            is_ready=True
                        ))

            await self.db_interaction.add_tournament_team(
                captain_id=captain.id,
                players=players,
                name=team.name,
                photo=team.photo
            )


async def add_test_tournament_teams(self, count_team: int):
    last_user_id = await self.db_interaction.get_last_user_id()
    discord = f'username#{last_user_id}'
    fastcup = f'username{last_user_id}'
    username = f'username{last_user_id}'

    count = count_team * 5

    for i in range(1, count + 1, 1):
        user_id = last_user_id + i
        username = username + i

        await self.db_interaction.add_user(user_id=user_id, username=username)
        await self.db_interaction.add_member(user_id=user_id, last_name='Иванов', first_name='Иван',
                                             patronymic='Иванович',
                                             institution='СПК', member_type='STUDENT', group='Д192/2')
        await self.db_interaction.add_player(user_id=user_id, username=username, fastcup=fastcup, discord=discord,
                                             tg_username=username)
