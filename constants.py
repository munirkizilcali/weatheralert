import os

DATABASE_URL = os.path.abspath(os.path.join(os.path.dirname(__file__), "weather_data.db"))

WEATHER_API_ENDPOINT = "https://api.weather.gov/points"

ALERTUS_API_ENDPOINT = "https://demo.alertus.com/alertusmw/services/rest/activation/preset"

ALERTUS_USER = "devcandidate"

ALERTUS_PASS = "gooWmJQe"
