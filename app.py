import constants
from manager import WeatherDataManager
from flask import Flask, redirect, url_for, request, render_template
from flask_wtf.csrf import CSRFProtect

weather_data_manager = WeatherDataManager()
app = Flask(__name__)
app.config["SECRET_KEY"] = constants.SECRET_KEY
CSRFProtect(app)


@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")


@app.route("/", methods=["GET"])
def data():
    location = weather_data_manager.get_location()
    if location.get("city") is None or location.get("state") is None:
        return redirect(url_for("error"))
    data = weather_data_manager.get_latest_data()
    return render_template("data.html", data=data, location=location)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    # Update settings
    if request.method == "POST":
        lat = request.form.get("latitude")
        lng = request.form.get("longitude")
        freq = request.form.get("frequency")
        thresh = request.form.get("threshold")
        if all([lat, lng, freq, thresh]):
            weather_data_manager.update_settings(lat, lng, freq, thresh)
            weather_data_manager.update_weather_data()
            weather_data_manager.update_alerts()
        return redirect(url_for("data"))

    if request.method == "GET":
        data = weather_data_manager.get_settings()
        return render_template("settings.html", data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)        
