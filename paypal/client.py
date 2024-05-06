"""Libarys for module"""
from typing import Tuple, Literal
import uuid
import json
import base64
import datetime
import requests
from requests import Request
from paypal import exceptions

__all__: Tuple[str, ...] = (
    "Paypal",
)

class Paypal(object):
    """The base client class."""
    sandbox_base_url = "https://api-m.sandbox.paypal.com"
    live_base_url = "https://api.paypal.com"

    def __init__(
        self,
        env: Literal["sandbox", "deployment"],
        client_id: str,
        client_secret: str
    ):
        self.__env, self.env = env, env
        self.__base_url = self.sandbox_base_url if self.__env == "sandbox" else self.live_base_url if self.__env == "live" else None
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__token = None
        self.__token_request_at = None


    @staticmethod
    def generate_paypal_request_id(self):
        return str(uuid.uuid4())

    def basic_auth(self):
        """ Find basic auth, and returns base64 encoded """
        credentials = "{}:{}".format(self.__client_id, self.__client_secret)
        return base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    def generate_access_token_hash(self, authorization_code=None, refresh_token=None, headers=None) -> str:
        """ Generate new token by making a POST request """
        path = "/v1/oauth2/token"
        payload = "grant_type=client_credentials"

        if authorization_code is not None:
            payload = "grant_type=authorization_code&response_type=token&redirect_uri=urn:ietf:wg:oauth:2.0:oob&code=" + \
                authorization_code

        elif refresh_token is not None:
            payload = "grant_type=refresh_token&refresh_token" + refresh_token

        else:
            self.validate_access_token_hash()
            if self.__token is not None:
                # return cached copy
                return self.__token
            
        token = self.http_call(
            self.__base_url+path,
            "POST",
            data=payload,
            headers={
                "Authorization": "Basic " + self.basic_auth(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            })
        
        if refresh_token is None and authorization_code is None:
            # cache token for re-use in normal case
            self.__token_request_at = datetime.datetime.now()
            self.__token = token
        return token

    def validate_access_token_hash(self) -> bool:
        """ Checks if token duration has expired and if so resets token """
        if self.__token_request_at and self.__token and self.__token.get("expires_in") is not None:
            delta = datetime.datetime.now() - self.__token_request_at
            duration = (
                delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
            if duration > self.__token.get("expires_in"):
                self.__token = None

    def get_access_token(self, authorization_code=None, refresh_token=None, headers=None):
        """ Wraps get_token_hash for getting access token """
        return self.generate_access_token_hash(authorization_code, refresh_token, headers=headers or {})['access_token']
        
    def request(self, url: str, method: str, body=None, headers=None):
        """ Make HTTP call, formats response and does error handling. Uses self.http_call method. """

    def http_call(self, url, method, **kwargs):
        """ Makes a http call """
        response = requests.request(method, url, **kwargs)
        return self.validate_http_call(response, response.content.decode("utf-8"))
    
    def validate_http_call(self, response, content):
        """ Validate HTTP response """
        status = response.status_code

        if status in (301, 302, 303, 307):
            raise exceptions.Redirection(response, content)
        elif 200 <= status <= 299:
            return json.loads(content) if content else {}
        elif status == 400:
            raise exceptions.BadRequest(response, content)
        elif status == 401:
            raise exceptions.UnauthorizedAccess(response, content)
        elif status == 403:
            raise exceptions.ForbiddenAccess(response, content)
        elif status == 404:
            raise exceptions.ResourceNotFound(response, content)
        elif status == 405:
            raise exceptions.MethodNotAllowed(response, content)
        elif status == 409:
            raise exceptions.ResourceConflict(response, content)
        elif status == 410:
            raise exceptions.ResourceGone(response, content)
        elif status == 422:
            raise exceptions.ResourceInvalid(response, content)
        elif 401 <= status <= 499:
            raise exceptions.ClientError(response, content)
        elif 500 <= status <= 599:
            raise exceptions.ServerError(response, content)
        else:
            raise exceptions.ConnectionError(
                response, content, "Unknown response code: #{response.code}")
        
    def headers(self, refresh_token=None, headers=None):
        """ Default HTTP headers """
        token = self.generate_access_token_hash(refresh_token=refresh_token, headers=headers or {})

        return {
            "Authorization": f"{token['token_type']} {token['access_token']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
