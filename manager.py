import logging
import threading
import time

import dateutil.parser
import requests
from peewee import SqliteDatabase
from playhouse.shortcuts import model_to_dict

import constants
import db


class WeatherDataManager:
    def __init__(self):
        """
        Init the manager, set default values,
        create db table(if it already exists, this has not effect),
        and update the db with the latest data.
        """
        self.lat = None
        self.lng = None
        self.frequency = None
        self.thresh = None
        self.grid_url = None
        self._init_settings()

        # Init db
        self._db = SqliteDatabase(constants.DATABASE_URL)
        self._db.connect()
        self._db.create_tables([db.Weather])
        self._db.close()
        self.update_weather_data()

        # Start background worker to update weather data ever 'frequency' mins, as defined in settings.
        check_in_worker = threading.Thread(target=self._check_in)
        check_in_worker.daemon = True
        check_in_worker.start()

    def _check_in(self):
        while True:
            self.update_weather_data()
            time.sleep(int(self.frequency)*60)

    def _parse_settings(self):
        """Parse settings file and return dict containing only lat, lng, thresh, and frequency"""
        settings_dict = {}
        with open("settings.txt", "r") as f:
            for line in f:
                # Ignore comment lines
                if "#" in line:
                    continue
                # Strip empty values
                split_line = [l.strip() for l in line.split("=")]
                settings_dict[split_line[0]] = split_line[-1]
        return {key: value for key, value in settings_dict.items() if key}

    def _init_settings(self):
        """Call the weather api and set class attrs"""
        settings = self._parse_settings()
        lat, lng = settings.get("latitude"), settings.get("longitude")
        thresh, freq = settings.get("threshold_value"), settings.get(
            "check_in_frequency"
        )

        resp = requests.get(
            headers={"Accept": "application/cap+xml"},
            url=f"{constants.WEATHER_API_ENDPOINT}/{lat},{lng}",
        )
        if resp.ok:
            self._set_location(resp)
            grid_url =  resp.json().get("properties").get("forecastHourly")
            
        if not all([lat, lng, thresh, freq, grid_url]):
            raise Exception("Error setting values for WeatherDataUtil")

        self.lat = float(lat)
        self.lng = float(lng)
        self.thresh = int(thresh)
        self.frequency = int(freq)
        self.grid_url = grid_url

    def update_weather_data(self):
        """
        Call the weather gird endpoint, and fill the db with the latest 10 records of 3 hour segments
        """
        resp = requests.get(
            headers={"Accept": "application/cap+xml"}, url=self.grid_url
        )
        if resp.ok:
            forecast_list = resp.json().get("properties").get("periods")
            grouped_forecasts = zip(*[iter(forecast_list[:30])] * 3)
            for forecast1, forecast2, forecast3 in grouped_forecasts:
                # Its not defined which of the three hours the timestap should refer to. Currently its the first
                if (
                    not db.Weather.select()
                    .where(
                        (db.Weather.timestamp == self._parse_timestamp(forecast1.get("startTime"))) &
                        (db.Weather.latitude == self.lat) &
                        (db.Weather.longitude == self.lng)
                        )
                    .exists()
                ):
                    
                    instance = db.Weather.create(
                        timestamp=self._parse_timestamp(forecast1.get("startTime")),
                        latitude=self.lat,
                        longitude=self.lng,
                        first_forecast=forecast1.get("temperature"),
                        second_forecast=forecast2.get("temperature"),
                        third_forecast=forecast3.get("temperature"),
                    )
                    self._send_alert(instance)


    def update_settings(self, lat, lng, freq, thresh):
        """Update new cls attrs. If lat and lng have been changed, updated the gird_url"""
        if float(lat) != float(self.lat) or float(lng) != float(self.lng):
            resp = requests.get(
                headers={"Accept": "application/cap+xml"},
                url=f"{constants.WEATHER_API_ENDPOINT}/{lat},{lng}",
                )
            self._set_location(resp)
            if resp.ok:
                self.grid_url = resp.json().get("properties").get("forecastHourly")
                for d in db.Weather.select():
                    d.delete_instance()
                    
        self.lat = float(lat)
        self.lng = float(lng)
        self.thresh = int(thresh)
        self.frequency = int(freq)

    def _send_alert(self, model: db.Weather):
        """
        Check if any of the forcats temps are greater then the thresh, 
        if so, update the model instance
        """
        if any([
            model.first_forecast > int(self.thresh),
            model.second_forecast > int(self.thresh),
            model.third_forecast > int(self.thresh)
            ]):
            alert_data = self._get_first_preset_alert()            
            resp = requests.post(
                headers={'Content-type': 'application/json'},
                url=f"{constants.ALERTUS_POST_API_ENDPOINT}/{alert_data.get('id')}", 
                auth=(constants.ALERTUS_USER, constants.ALERTUS_PASS),
                )
            if resp.ok:
                model.alert_generated = True
                model.alert_id = resp.json()
                model.save()
        else:
            model.alert_generated = False
            model.alert_id = None
            model.save()

    def get_latest_data(self):
        return [model_to_dict(d) for d in db.Weather.select().order_by(db.Weather.id.desc()).limit(10)]

    def _parse_timestamp(self, timestamp):
        return dateutil.parser.parse(timestamp).strftime("%Y-%m-%d %H:%M")

    def _get_first_preset_alert(self):
        resp = requests.get(
            headers={'Content-type': 'application/json'},
            url=constants.ALERTUS_GET_ALERT_API_ENDPOINT, 
            auth=(constants.ALERTUS_USER, constants.ALERTUS_PASS)
            )
        if resp.ok:
            return resp.json()[0]
    
    def update_alerts(self):
        for forecast in db.Weather.select():
            self._send_alert(forecast)
                
    def _set_location(self, resp):
        if not resp.ok:
            self.city = None
            self.state = None
            return
        data = resp.json().get('properties').get("relativeLocation").get("properties")
        self.city = data.get("city")
        self.state = data.get("state")

    def get_settings(self):
        return {
            "latitude": self.lat,
            "longitude": self.lng,
            "threshold": self.thresh,
            "frequency": self.frequency,
        }
    
    def get_location(self):
        return {
            "city": self.city, 
            "state": self.state
        }
