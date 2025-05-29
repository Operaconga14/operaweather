from fastapi import FastAPI, HTTPException
from pyowm import OWM
from pyowm.utils.config import get_default_config
import os
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="OperaWeather API",
    description="API for fetching weather data from OpenWeatherMap",
    version="1.0.0",
)

config_dict = get_default_config()
config_dict['language'] = 'en'

apiKey = os.getenv("OPEN_WEATHER_API_KEY")
if not apiKey:
    raise ValueError("OpenWeather API key not found in environment variables")

owm = OWM(apiKey)
mgr = owm.weather_manager()

@app.get("/weather/{city}")
async def get_current_weather(city: str) -> Dict:
    """
    Get current weather information for a city with filtered important data
    """
    try:
        weather = mgr.weather_at_place(city).weather
        return {
            "status": "success",
            "data": {
                "temperature": {
                    "current": weather.temperature('celsius')['temp'],
                    "feels_like": weather.temperature('celsius')['feels_like']
                },
                "humidity": weather.humidity,
                "description": weather.detailed_status,
                "wind_speed": weather.wind()['speed'],
                "clouds": weather.clouds,
                "timestamp": datetime.fromtimestamp(weather.reference_time()).isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/temperature")
async def get_temperature(city: str) -> Dict:
    """
    Get detailed temperature information for a city
    """
    try:
        weather = mgr.weather_at_place(city).weather
        return {
            "status": "success",
            "data": {
                "current": weather.temperature('celsius')['temp'],
                "feels_like": weather.temperature('celsius')['feels_like'],
                "min": weather.temperature('celsius')['temp_min'],
                "max": weather.temperature('celsius')['temp_max'],
                "unit": "celsius"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/wind")
async def get_wind_info(city: str) -> Dict:
    """
    Get wind information for a city
    """
    try:
        weather = mgr.weather_at_place(city).weather
        wind_data = weather.wind()
        return {
            "status": "success",
            "data": {
                "speed": wind_data['speed'],
                "degree": wind_data.get('deg', None),
                "gust": wind_data.get('gust', None)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/atmosphere")
async def get_atmosphere_info(city: str) -> Dict:
    """
    Get atmospheric information (humidity, pressure, etc.) for a city
    """
    try:
        weather = mgr.weather_at_place(city).weather
        return {
            "status": "success",
            "data": {
                "humidity": weather.humidity,
                "pressure": weather.pressure['press'],
                "visibility": weather.visibility_distance,
                "clouds": weather.clouds
            }
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/forecast")
async def get_forecast(city: str) -> Dict:
    """
    Get 5-day weather forecast for a city
    """
    try:
        forecaster = mgr.forecast_at_place(city, '3h')
        forecast_list = []
        
        for weather in forecaster.forecast.weathers[:8]:  # Next 24 hours (8 * 3-hour intervals)
            forecast_list.append({
                "timestamp": datetime.fromtimestamp(weather.reference_time()).isoformat(),
                "temperature": weather.temperature('celsius')['temp'],
                "description": weather.detailed_status,
                "humidity": weather.humidity,
                "wind_speed": weather.wind()['speed']
            })
            
        return {
            "status": "success",
            "data": forecast_list
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")