from .config.config import FastAPI, API_URL, mgr, OWM, HTTPException, status

app = FastAPI(
    title="Weather API",
    description="API for fetching weather data from OpenWeatherMap",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the Weather API"}

@app.get(f"/{API_URL}/weather")
def get_weather(city: str):
    try:
        weather = mgr.weather_at_place(city).weather
        return  {
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get(f"/{API_URL}/weather/temperature")
def get_temperature(city: str):
    try:
        weather = mgr.weather_at_place(city).weather
        return {
            "status": "success",
            "data": {
                "city": city,
                "temperature": weather.temperature("celsius")["temp"],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@app.get(f"/{API_URL}/weather/humidity")
def get_humidity(city: str):
    try:
        weather = mgr.weather_at_place(city).weather
        return {
            "status": "success",
            "data": {
                "city": city,
                "humidity": weather.humidity,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@app.get(f"/{API_URL}/weather/wind")
def get_wind(city: str):
    try:
        weather = mgr.weather_at_place(city).weather
        return {
            "status": "success",
            "data": {
                "city": city,
                "wind_speed": weather.wind()["speed"],
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )