from pay_client.clients import AbstractPayClient
from pay_client.configs import AlipayConfig
from alipay.aop.api import DefaultAlipayClient, AlipayClientConfig

class AbstractAlipayClient(AbstractPayClient):
    def __init__(self, config: AlipayConfig):
        super().__init__(config)
    
    def init(self):
        self.client = DefaultAlipayClient()
