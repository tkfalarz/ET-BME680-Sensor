from setuptools import setup

setup(
    name='WeatherFactorsCollector',
    version='0.1.0-alpha',
    packages=['src', 'src.http_client', 'src.logging_service', 'src.sensor_readings_writer',
              'src.weather_factors_collector'],
    url='',
    license='Apache',
    author='Tomasz Falarz',
    author_email='tomasz.falarz@student.pk.edu.pl',
    description='An engineering thesis project',
    install_requires=['bme680']
)
