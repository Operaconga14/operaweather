from .config.config import FastAPI, API_URL, HTTPException, status, requests, BASE_WEATHER_URL, OPEN_WEATHER_API_KEY

app = FastAPI(
    title="Weather API",
    description="API for fetching weather data from OpenWeatherMap",
    version="1.0.0",
)


@app.get("/", tags=["Test"], summary="Testing Api Route")
def root():
    return HTTPException(status_code=status.HTTP_200_OK, detail="Welcome to the Weather API")


@app.get(f"/{API_URL}/weather/{{city}}", tags=["Weather"], summary="Get basic weather information for a city")
async def get_weather(city: str):
    try:
        params = {
            "q": city,
            "appid": OPEN_WEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_WEATHER_URL, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            return {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"]
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Weather data not found for city: {city}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get(f"/{API_URL}/weather/{{city}}/temperature", tags=["Weather"], summary="Get detailed temperature information for a city")
async def get_temperature(city: str):
    try:
        response = requests.get(BASE_WEATHER_URL, params={
            "q": city,
            "appid": OPEN_WEATHER_API_KEY
        })

        response.raise_for_status()
        data = response.json()

        return {
            "status": "success",
            "data": {
                "city": data["name"],
                "temperature": {
                    "celsius": round(data["main"]["temp"] - 273.15, 2),
                    "fahrenheit": round((data["main"]["temp"] - 273.15) * 9/5 + 32, 2)
                },
                "feels_like": {
                    "celsius": round(data["main"]["feels_like"] - 273.15, 2),
                    "fahrenheit": round((data["main"]["feels_like"] - 273.15) * 9/5 + 32, 2)
                },
                "min_temp": {
                    "celsius": round(data["main"]["temp_min"] - 273.15, 2),
                    "fahrenheit": round((data["main"]["temp_min"] - 273.15) * 9/5 + 32, 2)
                },
                "max_temp": {
                    "celsius": round(data["main"]["temp_max"] - 273.15, 2),
                    "fahrenheit": round((data["main"]["temp_max"] - 273.15) * 9/5 + 32, 2)
                }
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


@app.get(f"/{API_URL}/weather/{{city}}/atmosphere", tags=["Weather"], summary="Get atmospheric conditions for a city")
async def get_atmosphere(city: str):
    try:
        response = requests.get(BASE_WEATHER_URL, params={
            "q": city,
            "appid": OPEN_WEATHER_API_KEY
        })

        response.raise_for_status()
        data = response.json()

        return {
            "status": "success",
            "data": {
                "city": data["name"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", "Not available"),
                "clouds": data["clouds"]["all"] if "clouds" in data else "Not available"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get(f"/{API_URL}/weather/{{city}}/forecast", tags=["Weather"], summary="Get 5-day weather forecast for a city")
async def get_forecast(city: str):
    try:
        response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={
            "q": city,
            "appid": OPEN_WEATHER_API_KEY
        })

        response.raise_for_status()
        data = response.json()

        forecast_data = []
        for item in data["list"]:
            forecast_data.append({
                "datetime": item["dt_txt"],
                "temperature": {
                    "celsius": round(item["main"]["temp"] - 273.15, 2),
                    "fahrenheit": round((item["main"]["temp"] - 273.15) * 9/5 + 32, 2)
                },
                "weather": {
                    "main": item["weather"][0]["main"],
                    "description": item["weather"][0]["description"]
                },
                "humidity": item["main"]["humidity"],
                "wind": {
                    "speed": item["wind"]["speed"],
                    "direction": item["wind"]["deg"]
                }
            })

        return {
            "status": "success",
            "data": {
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecast": forecast_data
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get(f"/{API_URL}/weather/{{city}}/wind", tags=["Weather"], summary="Get wind conditions for a city")
async def get_wind(city: str):
    try:
        response = requests.get(BASE_WEATHER_URL, params={
            "q": city,
            "appid": OPEN_WEATHER_API_KEY
        })

        response.raise_for_status()
        data = response.json()

        return {
            "status": "success",
            "data": {
                "city": data["name"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"]["deg"],
                "wind_gust": data["wind"].get("gust", "Not available")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get(f"/{API_URL}/weather/{{city}}/sun", tags=["Weather"], summary="Get sunrise and sunset times for a city")
async def get_sun_times(city: str):
    try:
        response = requests.get(BASE_WEATHER_URL, params={
            "q": city,
            "appid": OPEN_WEATHER_API_KEY
        })

        response.raise_for_status()
        data = response.json()

        return {
            "status": "success",
            "data": {
                "city": data["name"],
                "sunrise": data["sys"]["sunrise"],
                "sunset": data["sys"]["sunset"],
                "day_length": data["sys"]["sunset"] - data["sys"]["sunrise"]
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
