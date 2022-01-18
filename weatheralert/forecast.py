import requests
import re

from typing import List
from weatheralert.alertus import activate_alert

# read the settings.txt file and load the values
def load_settings(file: str) -> List[str]:
    settings = []
    with open(file) as f:
        for line in f.readlines():
            settings.append(line)

    return settings


# curate the settings and turn it into a dictionary for easy access
def curated_settings(settings: List[str]) -> dict[str, float]:
    settings_dict = {}
    # goes through every entry in settings, only grabbing the information that we care about
    # while turning into a K,V pair such as {'latitude' : 39.23456}
    for line in settings:
        if "latitude" in line:
            # re.search() grabs a string between two characters, we only care about values
            # latitude, longitude, threshold and frequency
            settings_dict["latitude"] = float(re.search(r"= (.*)\n", line).group(1))
        elif "longitude" in line:
            settings_dict["longitude"] = float(re.search(r"= (.*)\n", line).group(1))
        elif "threshold_value" in line:
            settings_dict["threshold_value"] = float(
                re.search(r"= (.*)\n", line).group(1)
            )
        elif "check_in_frequency" in line:
            settings_dict["check_in_frequency"] = float(
                re.search(r"= (.*)\n", line).group(1)
            )
        else:
            pass

    return settings_dict


# allows the template to update settings based on new user input
def get_settings_dict() -> dict[str, float]:
    return curated_settings(load_settings("weatheralert/settings.txt"))


# we must generate the x, y and office coordinates with the given latitude and longitude
def generate_grid(latitude: float, longitude: float) -> dict[str, str]:
    # params holds the values we need to generate a forecast
    params = {}

    response = requests.get(
        f"https://api.weather.gov/points/{latitude},{longitude}"
    ).json()

    # store the params we need to make a forecast request
    params["grid x"] = response["properties"]["gridX"]
    params["grid y"] = response["properties"]["gridY"]
    params["office"] = response["properties"]["gridId"]

    return params


# after generating the grid location, we can generate a forecast
def generate_forecast_list(
    office: str,
    grid_x: str,
    grid_y: str,
    longitude: float,
    latitude: float,
    threshold_value: int,
) -> List[dict]:

    forecast_list = []
    # full forecast retrieves over 100 entries
    full_forecast = requests.get(
        f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly",
        headers={"Accept": "application/cap+xml"},
    ).json()

    # constructs a list of forecast to be added to the database based on integer check
    for i in range(0, 30, 3):

        first_forecast = full_forecast["properties"]["periods"][i]["temperature"]
        second_forecast = full_forecast["properties"]["periods"][i + 1]["temperature"]
        third_forecast = full_forecast["properties"]["periods"][i + 2]["temperature"]

        if (
            (first_forecast > threshold_value)
            or (second_forecast > threshold_value)
            or (third_forecast > threshold_value)
        ):
            alert_message = (
                "forecast value higher than threshold value found. initializing alert."
            )
            forecast_list.append(
                dict(
                    alert_generated=True,
                    alert_id=activate_alert(alert_message),
                    first_forecast=full_forecast["properties"]["periods"][i][
                        "temperature"
                    ],
                    longitude=longitude,
                    latitude=latitude,
                    second_forecast=full_forecast["properties"]["periods"][i + 1][
                        "temperature"
                    ],
                    third_forecast=full_forecast["properties"]["periods"][i + 2][
                        "temperature"
                    ],
                    timestamp=full_forecast["properties"]["periods"][i]["startTime"],
                )
            )
        else:
            forecast_list.append(
                dict(
                    alert_generated=False,
                    alert_id=0,
                    first_forecast=full_forecast["properties"]["periods"][i][
                        "temperature"
                    ],
                    longitude=longitude,
                    latitude=latitude,
                    second_forecast=full_forecast["properties"]["periods"][i + 1][
                        "temperature"
                    ],
                    third_forecast=full_forecast["properties"]["periods"][i + 2][
                        "temperature"
                    ],
                    timestamp=full_forecast["properties"]["periods"][i]["startTime"],
                )
            )

    return forecast_list
