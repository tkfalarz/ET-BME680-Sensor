import datetime
import logging
import pathlib
from datetime import datetime

DIR_NAME = "logs"


class LoggingService:
    def __init__(self, logger_name: str):
        self.__logger = logging.getLogger(logger_name)
        self.__logger.setLevel(logging.DEBUG)

        logs_dir_path = pathlib.Path(f"{pathlib.Path(__file__).parent.parent}/{DIR_NAME}")
        if not logs_dir_path.exists():
            logs_dir_path.mkdir()

        file_handler = logging.FileHandler(f"{logs_dir_path}/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}-logs.log")
        file_handler.setLevel(logging.NOTSET)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    def log_debug(self, message):
        self.__logger.debug(message)

    def log_info(self, message):
        self.__logger.info(message)

    def log_warning(self, message):
        self.__logger.warning(message)

    def log_error(self, message):
        self.__logger.error(message)

    def log_exception(self, message):
        self.__logger.exception(message)
