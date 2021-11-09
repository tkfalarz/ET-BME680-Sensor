import os

from ..logging_service import logging_service

DEVICE_NAME = "DEVICE_NAME"
SENSOR_NAME = "SENSOR_NAME"
SENSOR_LATITUDE = "SENSOR_LATITUDE"
SENSOR_LONGITUDE = "SENSOR_LONGITUDE"


class Device:
    def __init__(self):
        self.device_name = os.getenv(DEVICE_NAME, default=None)
        self.sensor_name = os.getenv(SENSOR_NAME, default=None)
        self.sensor_latitude = os.getenv(SENSOR_LATITUDE, default=None)
        self.sensor_longitude = os.getenv(SENSOR_LONGITUDE, default=None)
        self.__logger = logging_service.LoggingService(__name__)

    def is_valid(self) -> bool:
        if self.device_name is None:
            self.__logger.log_error(f"{DEVICE_NAME} variable is invalid")
            return False
        if self.sensor_name is None:
            self.__logger.log_error(f"{SENSOR_NAME} variable is invalid")
            return False
        if self.sensor_latitude is None:
            self.__logger.log_error(f"{SENSOR_LATITUDE} variable is invalid")
            return False
        if self.sensor_longitude is None:
            self.__logger.log_error(f"{SENSOR_LONGITUDE} variable is invalid")
            return False

        return True
