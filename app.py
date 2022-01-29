from utils import WeatherDataUtil
from flask import Flask, jsonify, redirect, url_for, request, render_template

weather_data_util = WeatherDataUtil()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def data():
    data = weather_data_util.get_latest_data()
    return render_template("data.html", data=data)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    # Update settings
    if request.method == "POST":
        lat = request.form.get("latitude")
        lng = request.form.get("longitude")
        freq = request.form.get("frequency")
        thresh = request.form.get("threshold")
        if all([lat, lng, freq, thresh]):
            weather_data_util.lat = lat
            weather_data_util.lng = lng
            weather_data_util.frequency = freq
            weather_data_util.thresh = thresh
        return redirect(url_for("data"))
    
    if request.method == "GET":
        data = weather_data_util.get_settings()
        return render_template("settings.html", data=data)
                       
if __name__ == "__main__":
    app.run()
