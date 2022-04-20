import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

import database_connection_manager
from weather_alert_logging import get_logger

logger = get_logger()


def load_settings_from_settings_txt_file():
    settings = {}
    try:
        with open('settings.txt', 'r') as f:
            file_lines = f.readlines()
            for line in file_lines:
                line = line.strip()
                if line.startswith('#') or line == '':
                    continue
                else:
                    key, value = line.split('=')
                    settings[key.strip()] = value.strip()
        settings = {
            'latitude': float(settings['latitude']),
            'longitude': float(settings['longitude']),
            'threshold_value': int(settings['threshold_value']),
            'check_in_frequency': int(settings['check_in_frequency'])
        }
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            logger.warning('settings.txt file not found. Creating new file.')
        else:
            logger.warning('Invalid settings.txt file. Creating new file.')
        settings = {
            'latitude': 25.877353,
            'longitude': -80.130049,
            'threshold_value': 80,
            'check_in_frequency': 60
        }
        update_settings_file(settings)
    return settings


def update_settings_file(settings):
    with open('settings.txt', 'w+') as f:
        f.writelines([
            '#Location Information\n',
            f"latitude = {settings['latitude']}\n",
            f"longitude = {settings['longitude']}\n",
            '\n',
            '#Application Settings\n',
            f"threshold_value = {settings['threshold_value']}\n",
            f"check_in_frequency = {settings['check_in_frequency']}\n",
        ])


def get_updated_forecasts_for_the_next_three_hours(settings):
    try:
        headers = {
            'accept': 'application/vnd.noaa.dwml+xml',
        }
        response = requests.get(
            "https://api.weather.gov/points/{},{}/".format(settings['latitude'], settings['longitude']),
            headers=headers)

        if response.status_code != 200:
            raise Exception(f'Invalid response code from NOAA API.{response.status_code}. details: {response.text}')
        response = response.json()
        response = response['properties']['forecastHourly']
        response = requests.get(response, headers=headers)

        if response.status_code != 200:
            raise Exception(f'Invalid response code from NOAA API.{response.status_code}, details: {response.text}')

        root = ET.fromstring(response.text)
        root = root[1][5][5]
        forecasts = [root[1], root[2], root[3]]
        for i, r in enumerate(forecasts):
            forecasts[i] = int(re.search(r'\d+', r.text).group(0))
    except Exception as e:
        logger.error(f'Error while getting forecasts from NOAA API. {e}')
        return None

    return forecasts


def generate_alert(settings):
    headers = {
        'accept': 'application/json; charset=UTF-8',
        'Content-Type': 'application/com.alertus-v1.0+json',
        'Authorization': f'Basic {os.environ.get("ALERTUS_CREDENTIALS")}'
    }

    data = '{"durationSeconds": 10,"presetName": "Dev Candidate - Evacuate","alertProfileId": 402,"presetId": 2206,' \
           '"clientVersion": "3.15.220207","alertProfileName": "Demo Alert Profile - Evacuate","sender": ' \
           '"devcandidate","clientName": "alertus","priority": 0,"text": "Temperature is going to be higher than ' + \
           str(int(settings['threshold_value'])) + ' ' \
                                                   'degrees. Evacuate immediately."}'

    response = requests.post("https://demo.alertus.com/alertusmw/services/rest/activation/preset", headers=headers,
                             data=data)

    return int(response.text)


def get_new_forecast_and_store_it():
    settings = load_settings_from_settings_txt_file()
    forecasts = get_updated_forecasts_for_the_next_three_hours(settings)
    if forecasts is None:
        return None
    alert_generated = False
    alert_id = None
    if any(forecast > settings['threshold_value'] for forecast in forecasts):
        alert_id = generate_alert(settings)
        alert_generated = True
    timestamp, long, lat, first_forecast, second_forecast, third_forecast, alert_generated, alert_id = datetime.timestamp(
        datetime.now()), settings['longitude'], settings['latitude'], forecasts[0], forecasts[1], forecasts[
                                                                                                           2], alert_generated, alert_id
    database_connection_manager.insert_forecast(timestamp, long, lat, first_forecast, second_forecast,
                                                third_forecast, alert_generated, alert_id)

    return {
        'timestamp': timestamp,
        'longitude': long,
        'latitude': lat,
        'first_forecast': first_forecast,
        'second_forecast': second_forecast,
        'third_forecast': third_forecast,
        'alert_generated': alert_generated,
        'alert_id': alert_id
    }
