from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from tg_bot.types.member import MemberType
from tg_bot.types.moderator import ModeratorRule
from tg_bot.types.institution import InstitutionType
from tg_bot.types.user import CreateRequestMember

from tg_bot.misc.phares import Phrases
from tg_bot.types.request import RequestStatus
from tg_bot.misc.scripts import notify_moderators, parse_callback


class CreatePlayer(StatesGroup):
    ENTER_USERNAME = State()
    ENTER_DISCORD = State()
    ENTER_FASCTCUP = State()


# MEMBER
async def cmd_start_member(msg: types.Message, state=FSMContext):
    await state.finish()

    register_kb = msg.bot.get('kb').get('register')

    if msg.text != '💠 Меню':
        menu_kb = await register_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=menu_kb)

    register_kb = msg.bot.get('kb').get('register')

    register_ikb = await register_kb.get_register_ikb()

    answer_text = Phrases.you_need_to_register_to_continue
    await msg.answer(answer_text, reply_markup=register_ikb)


async def repeated_request_member(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    register_kb = call.bot.get('kb').get('register')
    phrases = call.bot.get('phrases')

    choice_member_type_ikb = await register_kb.get_choice_member_type_ikb()
    await call.message.answer(text=phrases.first_step_registration, reply_markup=choice_member_type_ikb)
    await state.set_state(CreateRequestMember.CHOICE_MEMBER_TYPE)


async def cmd_start_user(msg: types.Message, state=FSMContext):
    await state.finish()

    user_id = msg.from_user.id
    db_model = msg.bot.get('db_model')
    register_kb = msg.bot.get('kb').get('register')
    phrases = msg.bot.get('phrases')
    username = msg.from_user.username

    if username is None:
        await msg.answer('Чтобы продолжить Вам необходимо указать username в настройках Вашего аккаунта Telegram.')
        return

    print(user_id)
    print(msg.chat.id)
    if not await db_model.is_user(user_id=user_id):
        await db_model.add_user(user_id=user_id, username=username)

    if msg.text != '💠 Меню':
        menu_kb = await register_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=menu_kb)

    if not await db_model.request_member_exist(user_id=user_id):
        choice_member_type_ikb = await register_kb.get_choice_member_type_ikb()
        await msg.answer(text=phrases.first_step_registration, reply_markup=choice_member_type_ikb)
        await state.set_state(CreateRequestMember.CHOICE_MEMBER_TYPE)
        return

    request_member = await db_model.get_request_member(user_id=user_id)

    if request_member.request_member_status == RequestStatus.FAIL:
        repeated_request_member_ikb = await register_kb.get_repeated_request_member_ikb()
        message_text = phrases.request_member_fail + request_member.comment
        await msg.answer(message_text, reply_markup=repeated_request_member_ikb)
    elif request_member.request_member_status == RequestStatus.PROCESS:
        await msg.answer(phrases.request_member_wait)
    elif request_member.request_member_status == RequestStatus.WAIT:
        await msg.answer(phrases.request_member_wait)


async def choice_member_type(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')

    call_data = call.data
    register_kb = call.message.bot.get('kb').get('register')
    db_model = call.bot.get('db_model')

    props = await parse_callback('choice_member_type', call_data)

    member_type = props.get('member_type')

    async with state.proxy() as data:
        data['member_type'] = member_type

    institution_type = InstitutionType.COLLEGE if member_type == MemberType.STUDENT else InstitutionType.SCHOOL

    institutions = await db_model.get_institutions(institution_type=institution_type)

    institution_ikb = await register_kb.get_choice_institution_ikb(institutions=institutions)

    await call.message.answer('<b>Выберите Ваше учебное заведение:</b>', reply_markup=institution_ikb)
    await CreateRequestMember.next()


async def choice_institution(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.answer('')

    phrases = call.bot.get('phrases')
    db_model = call.bot.get('db_model')

    call_data = call.data

    props = await parse_callback('choice_institution', call_data)

    institution_id = props.get('id')
    institution_type = props.get('type')

    institution = await db_model.get_institution(institution_id=institution_id, institution_type=institution_type)

    async with state.proxy() as data:
        data['institution'] = institution.name

    await call.message.answer(phrases.enter_fullname)
    await CreateRequestMember.next()


async def enter_fullname(msg: types.Message, state=FSMContext):
    fullname = msg.text

    for s in fullname:
        if s.isdigit():
            await msg.answer('<b>❌ Сообщение не должно содержать цифры!</b>\n\n'
                             '✅ Например: Иванов Иван Иванович')
            return

    fullname_data = fullname.split(' ')

    if len(fullname_data) != 3:
        await msg.answer('<b>❌ Введите полные данные!</b>\n\n'
                         '✅ Например: Иванов Иван Иванович')
        return

    async with state.proxy() as data:
        data['first_name'] = fullname_data[0].capitalize()
        data['last_name'] = fullname_data[1].capitalize()
        data['patronymic'] = fullname_data[2].capitalize()

    state_data = await state.get_data()
    member_type = state_data.get('member_type')

    student_text = '<b>Введите Вашу группу:</b>\n\n' \
                   '✅ Например: Д192/2'
    schoolboy_text = '<b>Введите Ваш класс:</b>\n\n' \
                     '✅ Например: 9А'
    message_text = student_text if member_type == MemberType.STUDENT else schoolboy_text

    await msg.answer(message_text)

    await CreateRequestMember.next()


async def enter_group(msg: types.Message, state=FSMContext):
    group = msg.text.upper()

    async with state.proxy() as data:
        data['group'] = group

    state_data = await state.get_data()
    member_type = state_data.get('member_type')

    student_text = '📷 Отправьте фото Вашего студенческого'
    schoolboy_text = '📷 Отправьте фото Вашего документа удостоверяющего личность'
    message_text = student_text if member_type == MemberType.STUDENT else schoolboy_text

    await msg.answer(message_text)
    await CreateRequestMember.next()


async def send_document_photo(msg: types.Message, state=FSMContext):
    document_photo = msg.photo[-1].file_id
    user_id = msg.from_user.id
    print(user_id)
    bot = msg.bot
    print(msg.photo[-1].file_id)
    db_model = bot.get('db_model')
    moderator_kb = bot.get('kb').get('moderator')
    state_data = await state.get_data()

    first_name = state_data.get('first_name')
    last_name = state_data.get('last_name')
    patronymic = state_data.get('patronymic')
    group = state_data.get('group')
    member_type = state_data.get('member_type')
    institution = state_data.get('institution')

    await db_model.add_request_member(user_id=user_id, first_name=first_name, last_name=last_name,
                                      patronymic=patronymic, group=group, document_photo=document_photo,
                                      institution=institution, member_type=member_type)

    ib_viewing_verif_request = await moderator_kb.get_view_verif_request_ikb(user_id=user_id)

    await notify_moderators(text='<b>🛎 Появилась новая анкета</b>', bot=bot, rule=ModeratorRule.VERIF_STUDENT,
                                 kb=ib_viewing_verif_request)
    await msg.answer(text='<b>✅ Ваша анкета отправлена на рассмотрение!</b>\n\n'
                          '🛎 Ожидайте уведомления!')
    await state.finish()


async def create_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    msg_title = '<b>Регистрация</b>\n\n'
    msg_text = 'Придумайте псевдоним:'
    text = msg_title + msg_text

    await call.message.answer(text=text)

    await state.set_state(CreatePlayer.ENTER_USERNAME)


async def enter_username(msg: types.Message, state=FSMContext):
    username = msg.text

    db_model = msg.bot.get('db_model')
    phrases = msg.bot.get('phrases')

    if await db_model.validation_player_username(username=username):
        await msg.answer(text=phrases.error_username_already_taken)
        return

    async with state.proxy() as data:
        data['username'] = username

    await msg.answer(text=phrases.enter_discrod)
    await CreatePlayer.next()


async def enter_discord(msg: types.Message, state=FSMContext):
    discord = msg.text

    db_model = msg.bot.get('db_model')
    phrases = msg.bot.get('phrases')

    if '#' not in discord:
        await msg.answer(text=phrases.error_enter_correct_discrod)
        return
    if await db_model.validation_player_discord(discord=discord):
        await msg.answer(text=phrases.error_discrod_already_taken)
        return

    async with state.proxy() as data:
        data['discord'] = discord

    await msg.answer(text=phrases.enter_fastcup)
    await CreatePlayer.next()


async def enter_fastcup(msg: types.Message, state=FSMContext):
    fastcup = msg.text

    user_id = msg.from_user.id
    db_model = msg.bot.get('db_model')
    menu_kb = msg.bot.get('kb').get('menu')
    phrases = msg.bot.get('phrases')

    if await db_model.validation_player_fastcup(fastcup=fastcup):
        await msg.answer(text=phrases.error_fastcup_already_taken)
        return

    state_data = await state.get_data()

    username = state_data.get('username')
    discord = state_data.get('discord')

    await db_model.add_player(user_id=user_id, username=username, tg_username=msg.from_user.username,
                              discord=discord, fastcup=fastcup)

    menu_ikb = await menu_kb.get_menu_ikb()
    await msg.answer(text=Phrases.menu, reply_markup=menu_ikb)
    await state.finish()


def register_handlers_register(dp: Dispatcher):
    dp.register_message_handler(cmd_start_member, commands=['start'], state='*', is_member=True)
    dp.register_message_handler(cmd_start_member, text='💠 Меню', state='*', is_member=True)
    dp.register_callback_query_handler(create_player, text=['create_player'], state='*', is_member=True)
    dp.register_message_handler(enter_username, state=CreatePlayer.ENTER_USERNAME, is_member=True)
    dp.register_message_handler(enter_discord, state=CreatePlayer.ENTER_DISCORD, is_member=True)
    dp.register_message_handler(enter_fastcup, state=CreatePlayer.ENTER_FASCTCUP, is_member=True)

    # USER
    dp.register_message_handler(cmd_start_user, commands=['start'], state='*', is_member=False)
    dp.register_message_handler(cmd_start_user, text='💠 Меню', state='*', is_member=False)
    dp.register_callback_query_handler(repeated_request_member, text=['repeated_request_member'], state='*',
                                       is_member=False)
    dp.register_callback_query_handler(choice_member_type, state=CreateRequestMember.CHOICE_MEMBER_TYPE,
                                       is_member=False)
    dp.register_callback_query_handler(choice_institution,
                                       state=CreateRequestMember.CHOICE_EDUCATIONAL_INSTITUTION, is_member=False)
    dp.register_message_handler(enter_fullname, state=CreateRequestMember.ENTER_FULLNAME, is_member=False)
    dp.register_message_handler(enter_group, state=CreateRequestMember.ENTER_GROUP, is_member=False)
    dp.register_message_handler(send_document_photo, state=CreateRequestMember.SEND_DOCUMENT_PHOTO,
                                content_types=types.ContentType.PHOTO, is_member=False)
