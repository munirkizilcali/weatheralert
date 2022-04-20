import sqlite3

from weather_alert_logging import get_logger

logger = get_logger()


def check_table_exists(connection: sqlite3.Connection):
    try:
        connection.execute("SELECT * FROM forecasts;")
    except sqlite3.OperationalError as e:
        if 'no such table' in e.args[0]:
            connection.execute(
                "CREATE TABLE forecasts (timestamp REAL, long REAL, lat REAL, first_forecast INT, second_forecast "
                "INTEGER, third_forecast INTEGER, alert_generated INTEGER, alert_id INTEGER );")
            connection.commit()


def get_connection():
    try:
        connection = sqlite3.connect('database.db')
        check_table_exists(connection)
        return connection
    except sqlite3.Error as e:
        logger.error(e)
        return None


def get_last_ten_forecasts():
    try:
        connection = get_connection()
        cursor = connection.execute("SELECT * FROM forecasts ORDER BY timestamp DESC LIMIT 10;")
        forecasts = cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(e)
        return None

    forecasts = [
        {'timestamp': forecast[0], 'longitude': forecast[1], 'latitude': forecast[2], 'first_forecast': forecast[3],
         'second_forecast': forecast[4], 'third_forecast': forecast[5], 'alert_generated': forecast[6],
         'alert_id': forecast[7] if forecast[7] else "NULL"} for forecast in forecasts]

    return forecasts


def insert_forecast(timestamp, long, lat, first_forecast,
                    second_forecast, third_forecast, alert_generated=0, alert_id=None):
    try:
        connection = get_connection()
        connection.execute("INSERT INTO forecasts VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                           (timestamp, long, lat, first_forecast, second_forecast, third_forecast, alert_generated,
                            alert_id))
        connection.commit()
    except sqlite3.Error as e:
        logger.error(e)
