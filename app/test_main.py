from fastapi.testclient import TestClient
from .main import app, get_openweather_response
from .utils import celcius_to_fahrenheit, unix_timestamp_to_datetime, response_parser

client = TestClient(app)

test_weather_api_response = {"coord":{"lon":-74.0817,"lat":4.6097},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03n"}],"base":"stations","main":{"temp":15.73,"feels_like":15.11,"temp_min":15.73,"temp_max":15.73,"pressure":1017,"humidity":67,"sea_level":1017,"grnd_level":738},"visibility":10000,"wind":{"speed":4.12,"deg":140},"clouds":{"all":40},"dt":1720567929,"sys":{"type":1,"id":8582,"country":"CO","sunrise":1720522214,"sunset":1720566756},"timezone":-18000,"id":3688689,"name":"Bogota","cod":200}


def test_celcius_to_fahrenheit():
    assert celcius_to_fahrenheit(0) == 32.0
    assert celcius_to_fahrenheit(100) == 212.0
    assert celcius_to_fahrenheit(37) == 98.6


def test_unix_timestamp_to_datetime():
    response = unix_timestamp_to_datetime(1720710900, delta_hours=-5).strftime('%Y-%m-%d %H:%M:%S')
    assert response == "2024-07-11 10:15:00"


def test_response_parser():
    response = response_parser(test_weather_api_response)
    response['requested_time'] = '11-07-2024 03:20:00 PM'

    expect_response = {
        'location_name': 'Bogota, CO', 
        'temperature_celsius': '15.73 °C', 
        'temperature_fahrenheit': '60.31 °K', 
        'wind': '4.12 m/s', 
        'weather': 'scattered clouds', 
        'pressure': '1017 hPa', 
        'humidity': '67%', 
        'sunrise': '05:50 AM', 
        'sunset': '06:12 PM', 
        'geo_coordinates': '[4.61, -74.08]', 
        'requested_time': '11-07-2024 03:20:00 PM'
    }
    assert response == expect_response


def test_get_openweather_response():
    weather_api_response, weather_api_response_json = get_openweather_response("Bogota", "co")
    assert weather_api_response.status_code == 200

    weather_api_response, weather_api_response_json = get_openweather_response("x+x+x+", "x+")
    assert weather_api_response.status_code == 404


def test_weather():
    response = client.get("/weather?city=Bogota&country=co")
    assert response.status_code == 200