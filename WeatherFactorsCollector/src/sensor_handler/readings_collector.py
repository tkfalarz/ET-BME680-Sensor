import sys
from datetime import datetime
from subprocess import PIPE, Popen
from time import sleep

import bme680
from src.logging_service import logging_service

FACTOR = 40.0
SMOOTH_SIZE = 10
SEA_LEVEL_PRESSURE = 1015.00
TEMPERATURE_OFFSET = -5
BME680_BURN_UP_TIME_SECS = 300
HUMIDITY_BASELINE = 40.0
HUMIDITY_WEIGHTING = 0.25


class ReadingsCollector:
    def __init__(self, sensor: bme680.BME680, device_name: str):
        if sensor is None:
            raise ValueError("Sensor not exist")
        if device_name is None:
            raise ValueError("Device name not exist")

        self.__sensor = sensor
        self.__device_name = device_name

        self.__gas_resistance_warm_up_data = []
        self.__gas_baseline = None
        self.__smoothed_cpu_temp = None

        self.__sensor.set_humidity_oversample(bme680.constants.OS_2X)
        self.__sensor.set_pressure_oversample(bme680.constants.OS_4X)
        self.__sensor.set_temperature_oversample(bme680.constants.OS_4X)
        self.__sensor.set_filter(bme680.constants.FILTER_SIZE_3)
        self.__sensor.set_gas_heater_temperature(320)
        self.__sensor.set_gas_heater_duration(150)
        self.__sensor.select_gas_heater_profile(0)

        self.__logger = logging_service.LoggingService(__name__)

    def chip_warm_up(self):
        self.__logger.log_info(f"Waiting {BME680_BURN_UP_TIME_SECS} s. for BME680 sensor warm-up.")
        try:
            cpu_temps = []

            while self.__sensor.get_sensor_data() is False or self.__sensor.data.heat_stable is False:
                continue

            for _ in range(1, BME680_BURN_UP_TIME_SECS + 1):
                self.__gas_resistance_warm_up_data.append(self.__sensor.data.gas_resistance)
                cpu_temps.append(self.__get_cpu_temperature())
                sleep(1)

            self.__smoothed_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
            self.__gas_baseline = sum(self.__gas_resistance_warm_up_data[-50:]) / 50.0

            self.__logger.log_info("BME680 successfully warmed-up")
        except (RuntimeError, IOError, ValueError) as ex:
            self.__logger.log_error("Sensor warm-up interruption")
            self.__logger.log_exception(ex)
            sys.exit()

    def collect_chip_readings(self):
        if self.__sensor.data.heat_stable is False \
                or self.__sensor.get_sensor_data() is None\
                or self.__gas_baseline is None:
            self.__logger.log_error("Sensor not ready yet!")
            sys.exit()

        humidity = self.__sensor.data.humidity
        timestamp = datetime.now()
        self.__logger.log_info("Weather factors collection...")

        return {
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            "deviceName": self.__device_name,
            "temperature": "{0:.2f}".format(self.__get_sensor_compensated_temperature()),
            "airQualityIndex": "{0:.2f}".format(self.__get_iaq_index(humidity)),
            "pressure": "{0:.2f}".format(self.__sensor.data.pressure),
            "humidity": "{0:.2f}".format(humidity)
        }

    def __get_sensor_compensated_temperature(self):
        raw_temp = self.__sensor.data.temperature
        comp_temp = raw_temp - ((self.__smoothed_cpu_temp - raw_temp) / FACTOR)
        return comp_temp

    def __get_iaq_index(self, humidity):
        gas = self.__sensor.data.gas_resistance
        gas_offset = self.__gas_baseline - gas

        humidity_offset = humidity - HUMIDITY_BASELINE

        # Calculate hum_score as the distance from the hum_baseline.
        if humidity_offset > 0:
            hum_score = (100 - HUMIDITY_BASELINE - humidity_offset)
            hum_score /= (100 - HUMIDITY_BASELINE)
            hum_score *= (HUMIDITY_WEIGHTING * 100)

        else:
            hum_score = (HUMIDITY_BASELINE + humidity_offset)
            hum_score /= HUMIDITY_BASELINE
            hum_score *= (HUMIDITY_WEIGHTING * 100)

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (gas / self.__gas_baseline)
            gas_score *= (100 - (HUMIDITY_WEIGHTING * 100))

        else:
            gas_score = 100 - (HUMIDITY_WEIGHTING * 100)

        # Calculate air_quality_score.
        air_quality_score = hum_score + gas_score
        return air_quality_score

    @staticmethod
    def __get_cpu_temperature():
        process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        output, _error = process.communicate()
        return float(output[output.index(b'=') + 1:output.rindex(b"'")])
