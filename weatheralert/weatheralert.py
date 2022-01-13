from flask import Blueprint, render_template, request, jsonify

from weatheralert.db import weatheralertDB
from weatheralert.db_handler import populate_db, db
from weatheralert.forecast import (
    generate_grid,
    get_settings_dict,
    generate_forecast_list,
)

bp = Blueprint("", __name__, url_prefix="")

# settings dict that we can update throughout the project
settings = get_settings_dict()

# setting up db
db = weatheralertDB()
db.create_table()

# route that handles sending necessary json data to our javascript function to perform
# data updating
@bp.route("/_updateData", methods=["GET"])
def updateData():
    grid = generate_grid(settings["latitude"], settings["longitude"])
    new_forecast_list = generate_forecast_list(
        grid["office"],
        grid["grid x"],
        grid["grid y"],
        settings["latitude"],
        settings["longitude"],
        settings["threshold_value"],
    )

    populate_db(db, new_forecast_list)

    return jsonify(
        lst=new_forecast_list,
        latitude=settings["latitude"],
        longitude=settings["longitude"],
        threshold_value=settings["threshold_value"],
    )


# display the data and highlight row that triggers warning
@bp.route("/", methods=["GET", "POST"])
def populate_home():
    grid = generate_grid(settings["latitude"], settings["longitude"])

    forecast_list = generate_forecast_list(
        grid["office"],
        grid["grid x"],
        grid["grid y"],
        settings["latitude"],
        settings["longitude"],
        settings["threshold_value"],
    )
    populate_db(db, forecast_list)

    # trigger updating our settings when html form sends a POST request
    if request.method == "POST":
        if request.form["update_settings"] == "Update":
            settings["latitude"] = float(request.form["latitude"])
            settings["longitude"] = float(request.form["longitude"])
            settings["threshold_value"] = int(request.form["threshold_value"])
            settings["check_in_frequency"] = int(request.form["check_in_frequency"])

            grid = generate_grid(settings["latitude"], settings["longitude"])
            forecast_list = generate_forecast_list(
                grid["office"],
                grid["grid x"],
                grid["grid y"],
                settings["latitude"],
                settings["longitude"],
                settings["threshold_value"],
            )

            populate_db(db, forecast_list)

    return render_template(
        "/home/home.html",
        lst=forecast_list,
        longitude=settings["longitude"],
        latitude=settings["latitude"],
        threshold_value=settings["threshold_value"],
        check_in_frequency=settings["check_in_frequency"],
    )
