import os

from dotenv import load_dotenv

load_dotenv()


ALERTUS_USER = os.getenv("ALERTUS_USER")

ALERTUS_PASS = os.getenv("ALERTUS_PASS")

SECRET_KEY = os.getenv("SECRET_KEY")

DATABASE_URL = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "weather_data.db")
)

WEATHER_API_ENDPOINT = "https://api.weather.gov/points"

ALERTUS_POST_API_ENDPOINT = (
    "https://demo.alertus.com/alertusmw/services/rest/activation/preset"
)

ALERTUS_GET_ALERT_API_ENDPOINT = (
    "https://demo.alertustech.com/alertusmw/services/rest/presets"
)
