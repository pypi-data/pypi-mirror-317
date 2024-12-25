from typing import Optional, Any
from pydantic import BaseModel, Field, HttpUrl, Json
from decimal import Decimal
from datetime import datetime

from pay_client.enums.order import DisplayMode, Status

class RefundUnified(BaseModel):
    out_trade_no: str
    out_refund_no: str
    reason: str
    pay_price: Decimal
    refund_price: Decimal
    notify_url: HttpUrl

class Refund(BaseModel):
    status: Status = Status.DEFAULT
    out_refund_no: Optional[str] = None
    channel_refund_no: Optional[str] = None
    success_time: Optional[datetime] = None
    raw_data: Optional[Json[Any]] = None
    channel_error_code: Optional[str] = None
    channel_error_message: Optional[str] = None
