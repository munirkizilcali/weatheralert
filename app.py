import json
from flask import Flask, jsonify, redirect, url_for
from utils import WeatherDataUtil

weather_data_util = WeatherDataUtil()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def data():
    data = weather_data_util.get_latest_data()
    return jsonify(data)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        return redirect(url_for("data"))
    if request.method == "GET":
        return "settings"


if __name__ == "__main__":
    app.run()
