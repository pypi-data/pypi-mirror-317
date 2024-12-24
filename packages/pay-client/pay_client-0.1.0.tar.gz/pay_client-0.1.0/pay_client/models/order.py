from typing import Optional, Any, Union
from pydantic import BaseModel, Field, HttpUrl, Json
from decimal import Decimal
from datetime import datetime

from pay_client.enums.order import DisplayMode, Status

class OrderUnified(BaseModel):
    out_trade_no: str
    subject: str = Field(..., max_length=256)
    body: str = Field(default=None, max_length=128)
    notify_url: HttpUrl
    return_url: Optional[HttpUrl] = None
    price: Decimal
    expire_time: datetime
    channel_extras: Optional[Json[Any]] = None
    display_mode: DisplayMode = DisplayMode.DEFAULT

class Order(BaseModel):
    status: Status = Status.DEFAULT
    out_trade_no: Optional[str] = None
    channel_order_no: Optional[str] = None
    channel_user_id: Optional[str] = None
    success_time: Optional[datetime] = None
    raw_data: Union[Json[Any], str, None] = None
    display_mode: DisplayMode = DisplayMode.DEFAULT
    display_content: Optional[str] = None
    channel_error_code: Optional[str] = None
    channel_error_message: Optional[str] = None

