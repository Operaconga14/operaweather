from fastapi import FastAPI, HTTPException, status
import os
from dotenv import load_dotenv
from pyowm import OWM

load_dotenv()

API_URL = os.getenv("API_URL")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY").strip('"')

owm = OWM(OPEN_WEATHER_API_KEY)
mgr = owm.weather_manager()