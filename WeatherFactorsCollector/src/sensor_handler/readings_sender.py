import requests

from ..environment_variables_settings import oauth, external_api
from ..logging_service import logging_service
from urllib.parse import urljoin


class ReadingsSender:
    def __init__(self, oauth_settings: oauth.OAuth, web_api_url: str):
        if oauth_settings is None:
            raise ValueError("Value oauth_settings not exist")
        if web_api_url is None:
            raise ValueError("Value api_settings not exist")

        self.__oauth_settings = oauth_settings
        self.__web_api_url = urljoin(web_api_url, "api/Readings")
        self.__bearer_token = ""
        self.__logger = logging_service.LoggingService(__name__)

    def send_readings(self, readings: str):
        response_status_code = self.__send_readings(readings, self.__bearer_token)

        if response_status_code is 401:
            self.__bearer_token = self.__request_for_bearer_token()
            response_status_code = self.__send_readings(readings, self.__bearer_token)

        if response_status_code in range(401, 499):
            self.__logger.log_error("Something went wrong with the request.")
        elif response_status_code in range(500, 599):
            self.__logger.log_error("Something went wrong with the server")

    def __request_for_bearer_token(self):
        request_content = {
            "client_id": self.__oauth_settings.client_id,
            "client_secret": self.__oauth_settings.client_secret,
            "audience": self.__oauth_settings.audience,
            "grant_type": self.__oauth_settings.grant_type
        }
        response = requests.post(self.__oauth_settings.token_url, json=request_content)

        if response.status_code is 401:
            self.__logger.log_error("Invalid credentials provided to environment configuration")
            return

        content = response.json()
        return f"{content['token_type']} {content['access_token']}"

    def __send_readings(self, readings: str, bearer_token: str) -> int:
        response = requests.post(
            self.__web_api_url,
            json=readings,
            headers={
                "Authorization": bearer_token
            })

        return response.status_code
