import datetime

from aiogram import Bot

from tg_bot.misc.matches import grouping, add_matches
from tg_bot.misc.scripts import notify_user
from tg_bot.models.db_model.models import Registration, Tournament
from tg_bot.types.registration import RegistrationStatus


async def close_registration(db_model, bot: Bot, registration: Registration):
    await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CLOSE)

    closing_date: datetime = datetime.datetime.now()
    await db_model.set_registration_closing_date(registration_id=registration.id, closing_date=closing_date)
    users: list = await db_model.get_users()

    await grouping(db_model=db_model)
    await add_matches(db_model=db_model)

    for user in users:
        await notify_user(
            text='Регистрация на турнир закончена <b>🔥 Burning Cup</b>\n\n'
                 'Команды и матчи можете посмотреть на сайте https://www.burning-cup.com',
            chat_id=user.id,
            bot=bot
        )
