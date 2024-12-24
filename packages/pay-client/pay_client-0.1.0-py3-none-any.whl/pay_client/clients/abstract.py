from pay_client.configs import Config
from pay_client.models.order import OrderUnified
from pay_client.models.refund import RefundUnified

class AbstractPayClient:
    def __init__(self, config):
        self.config = config

    def unified_order(self, data: OrderUnified):
        raise NotImplementedError

    def parse_order_notify(self, data):
        raise NotImplementedError

    def get_order(self, out_trade_no: str):
        raise NotImplementedError
    
    def unified_refund(self, data: RefundUnified):
        raise NotImplementedError

    def parse_refund_notify(self, data):
        raise NotImplementedError

    def get_refund(self, out_refund_no: str):
        raise NotImplementedError
