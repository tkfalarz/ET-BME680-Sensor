### Raspberry Pi Weather Factors Collector powered by Bosch™ Bme680 Sensor - Installation Guide

**What the script is?**

This script uses bme 680 sensor to gather some weather metrics. It sends the data to the particular [.NET API](https://github.com/tkfalarz/ET-Dotnet-API) by http protocol using M2M authentication. This project was created for my Engineering Thesis purposes and this is rather a showdown of my abilities than a real production solution. At this stage, be aware it can have some vulnerabilities (e.g.: using http instead of https protocol, no code injections expected ;) ). Feel free to contribute or suggest some tips. Have a good day :)

**Prerequisites:**
- Raspberry Pi device with network card included
- Python at least version 3 installed
- Bme 680 sensor
- 4x wires

**1. Connect your sensor with Raspberry Pi**

Here is an example how to connect sensor to the Rasbperry Pi Zero W device. You can find the device pinout on the internet.

![pi-and-bme680_bb](https://user-images.githubusercontent.com/9446202/148239576-1c41e496-e776-43a8-97e4-2b6593195a8e.jpg)


**2. Clone the repo into your device**

But first, ensure you have git installed. After that, open the terminal and clone the repo by using
```
https://github.com/tkfalarz/ET-BME680-Sensor.git
```

**3. Set required environment variables**

Open `/etc/rc.local` and add required environment variables. Use `nano` or `vim`.

Important! The device needs M2M authentication, so it is needed to have a security platform configured at first, e.g.: `https://auth0.com/`

List of required environment variables to add:
| Environment Variable | Description |
| - | - |
| WEB_API_OAUTH_TOKEN_URL | OAuth M2M token URL |
| WEB_API_OAUTH_CLIENT_ID | Client identity |
| WEB_API_OAUTH_CLIENT_SECRET | Client secret |
| WEB_API_OAUTH_AUDIENCE | OAuth audience |
| WEB_API_OAUTH_GRANT_TYPE | Token grand type |
| WEB_API_URL | Url of web application consuming the factors |
| DEVICE_NAME | Familiar name of the device |
| SENSOR_NAME | Name of the sensor |
| SENSOR_LATITUDE | Sensor latitude coorinate |
| SENSOR_LONGITUDE | Sensor longitude coordinate |

**4. Set script autorun at the system startup**

open `/etc/rc.local` and paste the code below, after environment variables setup
```
python3 /path-to-repo/WeatherFactorsCollector/src/__main__.py &
```

**5. Restart the device**

Use `reboot` to restart the device and ensure the script is running by visiting `WeatherFactorsCollector/src/logs` or `WeatherFactorsCollector/src/readings` catalog.
It should be created a new file, with the current datetime in the each directory.
