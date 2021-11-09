import os

from src.logging_service import logging_service

WEB_API_URL = "WEB_API_URL"


class ExternalApi:
    def __init__(self):
        self.api_url = os.getenv(WEB_API_URL, default=None)
        self.__logger = logging_service.LoggingService(__name__)

    def is_valid(self) -> bool:
        if self.api_url is None:
            self.__logger.log_error(f"{WEB_API_URL} variable is invalid")
            return False

        return True
