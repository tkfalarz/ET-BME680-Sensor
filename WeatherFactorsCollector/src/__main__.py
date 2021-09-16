import time
import uuid
import bme680

from logging_service import logging_service
from sensor_readings_writer import sensor_readings_writer
from weather_factors_collector import weather_factors_collector

if __name__ == '__main__':
    logger = logging_service.LoggingService(__name__)
    writer = sensor_readings_writer.SensorReadingsWriter()

    sensor = None
    try:
        logger.log_info("Connecting with BME680...")
        sensor = bme680.BME680(bme680.constants.I2C_ADDR_PRIMARY)
        logger.log_info("Successfully connected with BME680!")
    except (RuntimeError, IOError, ValueError) as ex:
        logger.log_error("Failed to connect with BME680. Terminating...")
        logger.log_exception(ex)
        exit()

    try:
        collector = weather_factors_collector.WeatherFactorsCollector(sensor)
        collector.chip_warm_up()

        while True:
            readings = collector.collect_chip_readings(hex(uuid.getnode()))
            writer.save_to_file(readings)
            time.sleep(1800)
    except BaseException as ex:
        logger.log_exception(f"{ex}")
