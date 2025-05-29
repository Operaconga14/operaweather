from .config.config import FastAPI, API_URL

app = FastAPI(
    title="Weather API",
    description="A simple weather API",
    version="1.0.0"
)

@app.get(f"{API_URL}/weather")
def get_weather(city: str):
    return {"city": city, "weather": "sunny"}