from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .request_kb import RequestKb
from tg_bot.types.request import RequestStatus


class RequestTeamKb(RequestKb):
    __request_type: str = "team"

    # Get
    __ib_get_all: InlineKeyboardButton = InlineKeyboardButton(text="Получить всё", callback_data="get_all?type=team")

    __ib_get_by_status_wait: InlineKeyboardButton = InlineKeyboardButton(text="В ожидании",
                                                                         callback_data="get_by?type=team&by=status&value=wait")
    __ib_get_by_status_success: InlineKeyboardButton = InlineKeyboardButton(text="Успешно",
                                                                            callback_data="get_by?type=team&by=status&value=success")
    __ib_get_by_status_process: InlineKeyboardButton = InlineKeyboardButton(text="В процессе",
                                                                            callback_data="get_by?type=team&by=status&value=process")
    __ib_get_by_status_cancel: InlineKeyboardButton = InlineKeyboardButton(text="Отменено",
                                                                           callback_data="get_by?type=team&by=status&value=cancel")
    __ib_get_by_status_fail: InlineKeyboardButton = InlineKeyboardButton(text="Провал",
                                                                         callback_data="get_by?type=team&by=status&value=fail")

    async def get_ib(self, text: str, method: str, request_id: str = None,
                     status: str = None) -> InlineKeyboardButton:
        callback_data: str = f"{method}?type={self.__request_type}"

        if request_id:
            callback_data += f"&id={request_id}"
        if status:
            callback_data += f"&status={status}"

        ib: InlineKeyboardButton = InlineKeyboardButton(text=text, callback_data=callback_data)

        return ib

    async def choice_status(self, request_id: str) -> InlineKeyboardMarkup:
        choice_status_ikb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)

        ib_set_status_fail: InlineKeyboardButton = await self.get_ib(
            text=RequestStatus.FAIL, method=self.__method_set_status,
            request_id=request_id,
            status=RequestStatus.FAIL
        )
        ib_set_status_success: InlineKeyboardButton = await self.get_ib(
            text=RequestStatus.SUCCESS, method=self.__method_set_status,
            request_id=request_id,
            status=RequestStatus.SUCCESS
        )
        ib_set_status_cancel: InlineKeyboardButton = await self.get_ib(
            text=RequestStatus.CANCEL, method=self.__method_set_status,
            request_id=request_id,
            status=RequestStatus.CANCEL
        )
        choice_status_ikb.add(ib_set_status_fail).add(ib_set_status_success).add(ib_set_status_cancel)

        return choice_status_ikb

    async def view(self, request_status: str, request_id: str) -> InlineKeyboardMarkup:
        view_ikb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3)

        if request_status == RequestStatus.PROCESS or request_status == RequestStatus.WAIT:
            ib_moderation_yes: InlineKeyboardButton = await self.get_ib(text="Да",
                                                                        method=self.__method_moderation,
                                                                        request_id=request_id,
                                                                        status=RequestStatus.SUCCESS)
            ib_moderation_no: InlineKeyboardButton = await self.get_ib(text="Нет",
                                                                       method=self.__method_moderation,
                                                                       request_id=request_id,
                                                                       status=RequestStatus.FAIL)
            ib_moderation_postpone: InlineKeyboardButton = await self.get_ib(text="Отложить",
                                                                             method=self.__method_moderation,
                                                                             request_id=request_id,
                                                                             status=RequestStatus.WAIT)
            view_ikb.add(ib_moderation_yes).add(ib_moderation_no).add(ib_moderation_postpone)
        else:
            ib_set_status: InlineKeyboardButton = await self.get_ib(text="Изменить статус",
                                                                    method=self.__method_choice_status,
                                                                    request_id=request_id)
            view_ikb.add(ib_set_status)

        return view_ikb

    async def get_all(self, requests: list) -> InlineKeyboardMarkup:
        ikb_all_requests: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)

        for request in requests:
            request_text: str = f"{request.get('date')} {request.get('item').get('team_name')} {request.get('status')}"
            ib_request: InlineKeyboardButton = await self.get_ib(text=request_text,
                                                                 method=self.__method_view,
                                                                 request_id=request.get('id'),
                                                                 status=request.get('status'))
            ikb_all_requests.add(ib_request)

        return ikb_all_requests

    async def get_by(self) -> InlineKeyboardMarkup:
        get_by_status_bs: list = [
            self.__ib_get_by_status_wait,
            self.__ib_get_by_status_success,
            self.__ib_get_by_status_process,
            self.__ib_get_by_status_cancel,
            self.__ib_get_by_status_fail
        ]

        ikb_get_by_status: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1).add(*get_by_status_bs)

        return ikb_get_by_status

    async def get_menu(self) -> InlineKeyboardMarkup:
        ikb_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)

        ib_menu: InlineKeyboardButton = await self.get_ib(method=self.__method_get_all,
                                                          text="Все")
        ikb_menu.add(ib_menu)

        return ikb_menu

    async def moderation(self) -> InlineKeyboardMarkup:
        pass

    async def set(self) -> InlineKeyboardMarkup:
        pass
