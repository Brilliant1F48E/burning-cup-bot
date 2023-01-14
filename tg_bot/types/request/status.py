from enum import Enum


class RequestStatus(Enum):
    SUCCESS: str = 'SUCCESS'
    FAIL: str = 'FAIL'
    CANCEL: str = 'CANCEL'
    WAIT: str = 'WAIT'
    PROCESS: str = 'PROCESS'
