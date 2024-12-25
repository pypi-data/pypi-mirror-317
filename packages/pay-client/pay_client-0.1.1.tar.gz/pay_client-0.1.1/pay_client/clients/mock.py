from datetime import datetime
from typing import override
from pay_client.clients import AbstractPayClient
from pay_client.models.order import Order
from pay_client.enums.order import Status
from pay_client.models.refund import Refund


class MockPayClient(AbstractPayClient):
    @override
    def unified_order(self, data):
        return Order(
            status=Status.SUCCESS,
            channel_order_no=f'MOCK-P-{data.out_trade_no}', 
            channel_user_id='',
            success_time=datetime.now(),
            out_trade_no=data.out_trade_no,
            raw_data='MOCK_SUCCESS',
        )
    
    @override
    def get_order(self, out_trade_no):
        return Order(
            status=Status.SUCCESS,
            channel_order_no=f'MOCK-P-{out_trade_no}', 
            channel_user_id='',
            success_time=datetime.now(),
            out_trade_no=out_trade_no,
            raw_data='MOCK_SUCCESS',
        )
    
    @override
    def unified_refund(self, data):
        return Refund(
            status=Status.SUCCESS,
            channel_refund_no=f'MOCK-R-{data.out_refund_no}', 
            success_time=datetime.now(),
            out_refund_no=data.out_refund_no,
            raw_data='MOCK_SUCCESS',
        )
    
    @override
    def get_refund(self, out_refund_no):
        return Refund(
            status=Status.SUCCESS,
            channel_refund_no=f'MOCK-R-{out_refund_no}', 
            success_time=datetime.now(),
            out_refund_no=out_refund_no,
            raw_data='MOCK_SUCCESS',
        )
    