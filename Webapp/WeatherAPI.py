# check today weather by openweather api
import requests

city = 'Canberra'
openweather_API_KEY = 'af498f5cac3691870fb684b490ad9408'
openweather_API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_API_KEY}&units=metric"


def check_today_weather_values():
    global openweather_API_URL

    response = requests.get(openweather_API_URL)

    if response.status_code == 200:
        data = response.json()

        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        wind_dir = data['wind']['deg']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
    else:
        return "Weather API error!"

    return min_temp, max_temp, wind_dir, wind_speed, humidity, pressure


def check_temperature_now():
    global openweather_API_URL
    response = requests.get(openweather_API_URL)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
    else:
        return "Weather API error!"

    return temp