from app import app
from flask import render_template, request
from .fetch_data import extract_variables,set_variables
from .models import ForecastModel


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        set_variables(request.form.to_dict())

    var_data = extract_variables()
    table = get_table()
    frequency = int(var_data['check_in_frequency']) * 1000
    print(frequency)
    return render_template('index.html', data=var_data, table=table, frequency=frequency)


@app.route('/get_table', methods=['GET', 'POST'])
def get_table():
    forecast_data = ForecastModel.query.order_by(ForecastModel.id.desc()).limit(10).all()
    li = []
    for data in forecast_data:
        li.append({'timestamp': data.timestamp, 'first_forecast': data.first_forecast,
                   'second_forecast': data.second_forecast, 'third_forecast': data.third_forecast,
                   'id': data.id, 'long': data.long, 'lat': data.lat, 'alert_id': data.alert_id,
                   'alert_generated': data.alert_generated})
    rec = render_template('table.html', li=li)
    return rec
