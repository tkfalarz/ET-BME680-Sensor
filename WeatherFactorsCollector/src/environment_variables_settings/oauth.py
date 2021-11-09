import os

from src.logging_service import logging_service

OAUTH_AUDIENCE = "WEB_API_OAUTH_AUDIENCE"
OAUTH_TOKEN_URL = "WEB_API_OAUTH_TOKEN_URL"
OAUTH_GRANT_TYPE = "WEB_API_OAUTH_GRANT_TYPE"
OAUTH_CLIENT_ID = "WEB_API_OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "WEB_API_OAUTH_CLIENT_SECRET"


class OAuth:
    def __init__(self):
        self.token_url = os.getenv(OAUTH_TOKEN_URL, default=None)
        self.grant_type = os.getenv(OAUTH_GRANT_TYPE, default=None)
        self.client_id = os.getenv(OAUTH_CLIENT_ID, default=None)
        self.client_secret = os.getenv(OAUTH_CLIENT_SECRET, default=None)
        self.audience = os.getenv(OAUTH_AUDIENCE, default=None)
        self.__logger = logging_service.LoggingService(__name__)

    def is_valid(self) -> bool:
        if self.audience is None:
            self.__logger.log_error(f"{OAUTH_AUDIENCE} variable is invalid")
            return False
        if self.client_id is None:
            self.__logger.log_error(f"{OAUTH_CLIENT_ID} variable is invalid")
            return False
        if self.client_secret is None:
            self.__logger.log_error(f"{OAUTH_CLIENT_SECRET} variable is invalid")
            return False
        if self.token_url is None:
            self.__logger.log_error(f"{OAUTH_TOKEN_URL} variable is invalid")
            return False
        if self.grant_type is None:
            self.__logger.log_error(f"{OAUTH_GRANT_TYPE} variable is invalid")
            return False

        return True
