from .config.config import FastAPI, API_URL, HTTPException, status, requests, BASE_WEATHER_URL, OPEN_WEATHER_API_KEY

app = FastAPI(
    title="Weather API",
    description="API for fetching weather data from OpenWeatherMap",
    version="1.0.0",
)


@app.get("/", tags=["Test"], summary="Testing Api Route")
def root():
    return HTTPException(status_code=status.HTTP_200_OK, detail="Welcome to the Weather API")


@app.get("/weather/{city}", tags=["Weather"], summary="Get Weather Details")
def get_weather(city: str):
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
