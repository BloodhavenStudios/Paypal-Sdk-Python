"""Libarys for module"""
from typing import Tuple
import uuid
import base64

__all__: Tuple[str, ...] = (
    "Paypal",
)

class _BaseClient:
    """The base client class."""
    sandbox_base_url = "https://api-m.sandbox.paypal.com"
    live_base_url = "https://api.paypal.com"

    @staticmethod
    def generate_paypal_request_id(self):
        return str(uuid.uuid4())

    def basic_auth(self):
        credentials = "{}:{}".format(self.__client_id, self.__client_secret)
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    def generate_access_token(self):
        self.__client_id

    def post()

class Paypal(_BaseClient):

    def __init__(
        self,
        env: str["sandbox", "deployment"],
        client_id: str,
        client_secret: str
    ):
        self.__env = env
        self.__client_id = client_id
        self.__client_secret = client_secret

    def create_order(self):
        tk = self.generate_access_token()
