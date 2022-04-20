import json

import requests_cache
from flask import Flask, render_template, request

import database_connection_manager
from utils import load_settings_from_settings_txt_file, update_settings_file, get_new_forecast_and_store_it
from weather_alert_logging import get_logger

app = Flask(__name__)

requests_cache.install_cache('cache', backend='sqlite', expire_after=600)

app.logger = get_logger()


@app.route('/')
def index():
    """
    This is the main page of the app.
    Here the user can see the last ten forecasts saved in the database.
    :return: The rendered data template.
    """
    forecasts = database_connection_manager.get_last_ten_forecasts()
    if forecasts is None:
        app.logger.error('Could not fetch forecasts from database')
        return {'error': 'Could not fetch the forecasts from database.'}, 500
    settings = load_settings_from_settings_txt_file()
    return render_template('data.html', forecasts=forecasts, settings=settings)


@app.route('/settings/', methods=['GET', 'POST'])
def settings_view():
    """
    This is the settings page of the app.
    Here the user can change the settings of the app.
    :return: The rendered settings template.
    """
    if request.method == 'POST':
        settings = request.form
        update_settings_file(settings)
        app.logger.info(f'Settings updated successfully, new settings: {settings}')
    else:
        settings = load_settings_from_settings_txt_file()
    return render_template('settings.html', settings=settings)


@app.route('/forecast/', methods=['GET'])
def forecast_view():
    """
    Endpoint to fetch the forecast for the next three hours and store it in the database.
    :return: The forecast as a json object with the fields used to store them in the database.
    """
    new_forecast = get_new_forecast_and_store_it()
    if new_forecast is None:
        app.logger.error('Could not fetch new forecast')
        return {'error': 'Could not fetch the forecast.'}, 500
    forecasts = {"timestamp": new_forecast['timestamp'], "longitude": new_forecast['longitude'],
                 "latitude": new_forecast['latitude'], "first_forecast": new_forecast['first_forecast'],
                 "second_forecast": new_forecast['second_forecast'], "third_forecast": new_forecast['third_forecast'],
                 'alert_generated': new_forecast['alert_generated'], 'alert_id': new_forecast['alert_id']}
    app.logger.info(f'New forecast fetched successfully, new forecast: {forecasts}')
    return json.dumps(forecasts)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
