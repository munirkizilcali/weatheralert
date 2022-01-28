from playhouse.shortcuts import model_to_dict
from peewee import SqliteDatabase
import time
import threading
import requests
import constants
import db

class WeatherDataUtil:
    def __init__(self):
        """
        Init the util, cache the weather grid url, 
        create db table(if they exist already, this has not effect), 
        and update the db with the latest data.
        """
        self.lat = None
        self.lng = None
        self.frequency = None
        self.thresh = None
        self.grid_url = self._set_weather_grid()
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
            time.sleep(self.frequency*60)
        
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
            

    def _set_weather_grid(self):
        """Call the weather api, set class values and return the weather gird endpoint"""
        settings = self._parse_settings()
        lat, lng = settings.get("latitude"), settings.get("longitude")
        thresh, freq = settings.get("threshold_value"), settings.get("check_in_frequency")
        if not all([lat, lng, thresh, freq]):
            raise Exception("Error parsing info from settings.txt. No lat or lng")
        
        self.lat = float(lat)
        self.lng = float(lng)
        self.thresh = int(thresh)
        self.frequency = int(freq)
        resp = requests.get(headers={"Accept": "application/cap+xml"}, url=f"{constants.WEATHER_API_ENDPOINT}/{lat},{lng}")
        if resp.ok:
            props = resp.json().get("properties")
            return props.get("forecastHourly")
            
        
    def update_weather_data(self):
        """
        Call the weather gird endpoint, and fill the db with the latest 10 records
        """
        resp = requests.get(headers={"Accept": "application/cap+xml"}, url=self.grid_url)
        if resp.ok:
            forcast_list = resp.json().get("properties").get("periods")
            grouped_forcasts = zip(*[iter(forcast_list)] * 3)
            for forcast1, forcast2, forcast3 in grouped_forcasts:
                #Its not defined which of the three hours the timestap should refer to. Currently its the first
                if not db.Weather.select().where(db.Weather.timestamp==forcast1.get("startTime")).exists():
                    instance = db.Weather.create(
                        timestamp=forcast1.get("startTime"),
                        latitude=self.lat,
                        longitude=self.lng,
                        first_forcast=forcast1.get("temperature"),
                        second_forcast=forcast2.get("temperature"),
                        third_forcast=forcast3.get("temperature")                    
                    )
                    self._send_alert(instance)
                
    
    def update_settings(self, freq, thresh):
        """Update the settings file from user input"""
        self.thresh = thresh
        self.frequency = freq

    
    def _send_alert(self, model: db.Weather):
        """Check if alert should be sent, if so, update the model instance"""
        pass

    def get_latest_data(self):
        data = db.Weather.select().limit(10)
        return [model_to_dict(d) for d in data]
        
