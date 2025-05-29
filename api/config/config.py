from fastapi import FastAPI, HTTPException, status
import os
from dotenv import load_dotenv
import requests


load_dotenv()

API_URL = os.getenv("API_URL")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY").strip('"')
