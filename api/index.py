from .config.config import FastAPI, API_URL, HTTPException, status

app = FastAPI(
    title="Weather API",
    description="API for fetching weather data from OpenWeatherMap",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the Weather API"}