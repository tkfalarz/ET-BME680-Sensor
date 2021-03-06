import time
import bme680
import json

from logging_service import logging_service
from sensor_handler import readings_sender, readings_writer, readings_collector
from environment_variables_settings import oauth, device, external_api


def main():
    oauth_settings = oauth.OAuth()
    api_settings = external_api.ExternalApi()
    device_settings = device.Device()
    if not (oauth_settings.is_valid() and api_settings.is_valid() and device_settings.is_valid()):
        exit()

    logger = logging_service.LoggingService(__name__)
    writer = readings_writer.ReadingsWriter()
    sender = readings_sender.ReadingsSender(oauth_settings, api_settings.api_url)

    try:
        logger.log_info("Connecting with BME680...")
        sensor = bme680.BME680(bme680.constants.I2C_ADDR_PRIMARY)
        logger.log_info("Successfully connected with BME680!")

        collector = readings_collector.ReadingsCollector(sensor, device_settings.device_name)
        collector.chip_warm_up()

        while True:
            readings = collector.collect_chip_readings()
            writer.save_to_file(json.dumps(readings))
            sender.send_readings(readings)
            time.sleep(1800)

    except ValueError as value_error:
        logger.log_error(value_error)

    except (RuntimeError, IOError) as error:
        logger.log_error("Failed to connect with BME680. Terminating...")
        logger.log_exception(error)

    except BaseException as exception:
        logger.log_exception(exception)

    finally:
        exit()


if __name__ == '__main__':
    main()
