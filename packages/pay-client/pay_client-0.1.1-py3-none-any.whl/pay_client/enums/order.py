from enum import Enum, IntEnum

class DisplayMode(Enum):
    DEFAULT = 'default'
    URL = 'url'
    IFRAME = 'iframe'
    FORM = 'form'
    QR_CODE = 'qr_code'
    QR_CODE_URL = 'qr_code_url'
    BAR_CODE = 'bar_code'
    APP = 'app'

class Status(IntEnum):
    DEFAULT = -1
    WAITING = 0
    SUCCESS = 10
    REFUND = 20
    CLOSED = 30