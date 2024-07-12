from datetime import datetime, timezone, timedelta
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os, json


class Settings(BaseSettings):
    load_dotenv()    
    API_KEY: str = os.getenv('API_KEY')
    CONTACT_NAME: str = os.getenv('CONTACT_NAME')
    CONTACT_EMAIL: str = os.getenv('CONTACT_EMAIL')
    CONTACT_WEBSITE: str = os.getenv('CONTACT_WEBSITE')
    GITHUB_WEBSITE: str = os.getenv('GITHUB_WEBSITE')


def celcius_to_fahrenheit(celcius: float) -> float:
    return round(celcius * 9/5 + 32, 2)


def unix_timestamp_to_datetime(unix_timestamp: int, delta_hours: int= -5) -> datetime:
    utc_datetime = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    utc_delta = timedelta(hours=delta_hours)
    new_datetime = utc_datetime + utc_delta
    return new_datetime


def response_parser(weather_api_response) -> dict:
    response = {}
    response['location_name'] = f"{weather_api_response['name']}, {weather_api_response['sys']['country']}"
    response['temperature_celsius'] = f"{weather_api_response['main']['temp']} °C"
    response['temperature_fahrenheit'] = f"{celcius_to_fahrenheit(weather_api_response['main']['temp'])} °K"
    response['wind'] = f"{weather_api_response['wind']['speed']} m/s"

    response['weather'] = "No data"
    for weather in weather_api_response["weather"]:
        if response['weather'] == "No data":
            response['weather'] = weather["description"]
        else:
            response['weather'] = weather["description"] + ", " + response['weather']
    
    response['pressure'] = f"{weather_api_response['main']['pressure']} hPa"
    response['humidity'] = f"{weather_api_response['main']['humidity']}%"       
    response['sunrise'] = unix_timestamp_to_datetime(weather_api_response['sys']['sunrise']).strftime('%I:%M %p')
    response['sunset'] = unix_timestamp_to_datetime(weather_api_response['sys']['sunset']).strftime('%I:%M %p')
    response['geo_coordinates'] = f"[{round(weather_api_response['coord']['lat'], 2)}, {round(weather_api_response['coord']['lon'], 2)}]"

    utc_now = datetime.now(timezone.utc)
    utc_minus_5 = timedelta(hours=-5)
    current_time = utc_now + utc_minus_5   

    response['requested_time'] = current_time.strftime('%d-%m-%Y %I:%M:%S %p')    

    return response