from fastapi import FastAPI, Response, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import requests
from .utils import Settings, response_parser

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# App settings

settings = Settings()

description = """
Whether you need temperature, humidity, or weather conditions, our API provides accurate and up-to-date data. 

☀️ 🌤️ 🌥️ 🌦️ ☁️ 🌧️ 🌩️ 🌨️❄️

## Weather

You can **read current weather information for any city**.
"""

app = FastAPI(
    title="Weather API",
    description=description,
    summary="Weather API helps you retrieve the current weather information for any city.",
    version="1.0",
    contact={ "name": settings.CONTACT_NAME, "url": settings.CONTACT_WEBSITE, "email": settings.CONTACT_EMAIL },
    license_info={ "name": "GitHub Repo", "url": settings.GITHUB_WEBSITE },
    openapi_tags=[{ "name": "weather", "description": "Get the weather information for a city."},
                  { "name": "root", "description": "Welcome message"}]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# API routes

def get_openweather_response(city: str, country: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country.lower()}&units=metric&appid={settings.API_KEY}"    
    response = requests.get(url)
    return response, response.json()


@app.get("/", tags=["root"])
def home():
    return {"Hi, welcome to weather API": "check the documentation at /docs or /redoc"}


@app.get("/weather", tags=["weather"])
def weather(response: Response, 
            city: Annotated[str, Query(description="Name of the city")], 
            country: Annotated[str, Query(description="Two characters country code in lowercase. Example: co", 
                                          min_length=2,  max_length=2, pattern="^[a-z]{2}$" )]):
    """
    Get the weather information for a city.

    - **city**: Name of the city. Example: Bogota
    - **country**: Two characters country code in lowercase. Example: co
    """

    response.headers["content-type"] = "application/json"
    weather_api_response, weather_api_response_json = get_openweather_response(city, country)

    if weather_api_response_json['cod'] == str(status.HTTP_404_NOT_FOUND):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City not found')
    else:
        content = response_parser(weather_api_response_json)
        return content