import os

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "alertus_logs.log"))

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

ALERTUS_USER = "devcandidate"

ALERTUS_PASS = "gooWmJQe"
