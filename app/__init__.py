from flask import Flask, redirect
from .setup import Config
from app.fetch_data import extract_variables, get_data_from_noaa, send_alert
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(Config)
print(app.config)
db = SQLAlchemy(app)

from app import routes, models

from .models import ForecastModel

db.create_all()


def data_fetch():
    print('running scheduler!!')
    data_dic = extract_variables()
    global timer
    timer = data_dic['check_in_frequency']
    timestamp = datetime.now()
    long = data_dic['longitude']
    lat = data_dic['latitude']
    data = get_data_from_noaa(lat, long)
    alert_generated = False
    alert_id = None
    for key, value in data.items():
        if value > data_dic['threshold_value']:
            hours = {'first_forecast': 1, 'second_forecast': 2,
                    'third_forecast': 3}
            alert_id = send_alert(hours[key], value)
            if 'Error' not in alert_id:
                alert_generated = True
                break
    rec = ForecastModel(**data, timestamp=timestamp, long=long, lat=lat, alert_generated=alert_generated, alert_id=alert_id)
    db.session.add(rec)
    db.session.commit()


sched = BackgroundScheduler(daemon=True)
timer = extract_variables()['check_in_frequency']
sched.add_job(data_fetch, 'interval', seconds=int(timer))
sched.start()


