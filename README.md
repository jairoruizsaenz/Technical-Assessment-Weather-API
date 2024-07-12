# Weather API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/-pytest-3670A0?style=for-the-badge) 

A Weather API that uses the [OpenWeather](https://openweathermap.org/) API to retrieve the current weather by city.

You can try the API live by checking the weather for Bogota, Colombia using [this link](https://jairoruiz-weather-api.fly.dev/weather?city=Bogota&country=co). For more information, check the documentation [here](https://jairoruiz-weather-api.fly.dev/docs).

## Example

Requesting the information for Bogota, Colombia you should get a response similar to the following one:

```bash
GET /weather?city=Bogota&country=co
```

```bash
{
  "location_name": "Bogota, CO",
  "temperature_celsius": "14.73 °C",
  "temperature_fahrenheit": "58.51 °F",
  "wind": "3.09 m/s",
  "weather": "light rain",
  "pressure": "1017 hPa",
  "humidity": "82%",
  "sunrise": "05:50 AM",
  "sunset": "06:12 PM",
  "geo_coordinates": "[4.61, -74.08]",
  "requested_time": "12-07-2024 04:58:04 PM"
}
```

## Installation

### Prerequisites

- Python 3.10 installed on your system
- Docker (optional)

### Setting up a virtual environment

It's always a good practice to use a virtual environment for Python projects to manage dependencies. Here's how to set it up:

1. Open your terminal or command prompt.
2. Navigate to the root directory of this project.
3. Run the following command to create a virtual environment (replace `<myenv>` with your preferred environment name):
    ```bash
    python -m venv <myenv>
    ```

### Activate the virtual environment
On Windows:
```bash
myenv\Scripts\activate
```
On macOS and Linux:
```bash
source myenv/bin/activate
```

### Installing dependencies

Once you have activated the virtual environment, you can install the required dependencies using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### Create environment variables file

Add an environment file called `.env` in the `app` folder with the following variables:
```sh
CONTACT_NAME='John Doe'
CONTACT_EMAIL='johndoe@email.com'
CONTACT_WEBSITE='https://website/'
GITHUB_WEBSITE='https://github.com/johndoe'
# Get a key by creating an account at OpenWeather
API_KEY=''
```

### Testing the API

The file `test_main.py` in the `app` folder contains the tests for the API. Run the following command to execute the tests:
```bash
pytest
```

### Deployment

You can either run the API locally by running the following command in the `app` folder:
```bash
fastapi run main.py
```

This will deploy a server in production mode using the port 8000 and you'll be able to access the API at http://localhost:8000/

If you wish to change the port you can use the flag --port
```bash
fastapi run main.py --port <your_port>
```

Another option is to use Docker. The Dockerfile in the root folder contains the settings for the container.

First you'll need to create an image with the command:
```bash
docker build -t weather_api_image .
```

Then, run the container with the command:
```bash
docker run -d --name weather_api_container -p 8000:8000 weather_api_image
```

The API will be available at http://localhost:8000/