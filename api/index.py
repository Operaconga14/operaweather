from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from typing import Dict
from datetime import datetime
from mangum import Adapter

load_dotenv()

app = FastAPI(
    title="OperaWeather API",
    description="API for fetching weather data from OpenWeatherMap",
    version="1.0.0",
)

API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("OpenWeather API key not found in environment variables")

BASE_URL = "https://api.openweathermap.org/data/2.5"

def kelvin_to_celsius(kelvin: float) -> float:
    return round(kelvin - 273.15, 2)

# Add handler for AWS Lambda/Vercel
handler = Adapter(app)

@app.get("/")
async def root():
    """
    Root endpoint to verify API is working
    """
    return {"status": "ok", "message": "OperaWeather API is running"}

@app.get("/weather/{city}")
async def get_current_weather(city: str) -> Dict:
    """
    Get current weather information for a city with filtered important data
    """
    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "data": {
                "temperature": {
                    "current": kelvin_to_celsius(data["main"]["temp"]),
                    "feels_like": kelvin_to_celsius(data["main"]["feels_like"])
                },
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "clouds": data["clouds"]["all"],
                "timestamp": datetime.fromtimestamp(data["dt"]).isoformat()
            }
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/temperature")
async def get_temperature(city: str) -> Dict:
    """
    Get detailed temperature information for a city
    """
    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "data": {
                "current": kelvin_to_celsius(data["main"]["temp"]),
                "feels_like": kelvin_to_celsius(data["main"]["feels_like"]),
                "min": kelvin_to_celsius(data["main"]["temp_min"]),
                "max": kelvin_to_celsius(data["main"]["temp_max"]),
                "unit": "celsius"
            }
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/wind")
async def get_wind_info(city: str) -> Dict:
    """
    Get wind information for a city
    """
    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "data": {
                "speed": data["wind"]["speed"],
                "degree": data["wind"].get("deg"),
                "gust": data["wind"].get("gust")
            }
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/atmosphere")
async def get_atmosphere_info(city: str) -> Dict:
    """
    Get atmospheric information (humidity, pressure, etc.) for a city
    """
    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                "q": city,
                "appid": API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "status": "success",
            "data": {
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility"),
                "clouds": data["clouds"]["all"]
            }
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")

@app.get("/weather/{city}/forecast")
async def get_forecast(city: str) -> Dict:
    """
    Get 5-day weather forecast for a city
    """
    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "q": city,
                "appid": API_KEY
            }
        )
        response.raise_for_status()
        data = response.json()
        
        forecast_list = []
        for item in data["list"][:8]:  # Next 24 hours (8 * 3-hour intervals)
            forecast_list.append({
                "timestamp": datetime.fromtimestamp(item["dt"]).isoformat(),
                "temperature": kelvin_to_celsius(item["main"]["temp"]),
                "description": item["weather"][0]["description"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"]
            })
            
        return {
            "status": "success",
            "data": forecast_list
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail=f"City not found or error: {str(e)}")
