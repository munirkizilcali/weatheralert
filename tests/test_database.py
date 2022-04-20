from datetime import datetime

import database_connection_manager


def test_sqlite_database_connection():
    """
    Test if the database connection is working
    """
    connection = database_connection_manager.get_connection()
    assert connection is not None


def test_get_last_ten_forecasts():
    """
    Test if the last ten forecasts are returned
    """
    forecasts = database_connection_manager.get_last_ten_forecasts()
    assert forecasts and len(forecasts) <= 10


def test_insert_forecast():
    """
    Test if a forecast is inserted into the database
    """
    timestamp = datetime.timestamp(datetime.now())
    database_connection_manager.insert_forecast(timestamp, 25.877369, -80.343601,
                                                80, 81, 82, 0, None)
    forecasts = database_connection_manager.get_last_ten_forecasts()

    connection = database_connection_manager.get_connection()
    cursor = connection.execute("SELECT * FROM forecasts ORDER BY timestamp DESC LIMIT 1")
    latest_forecast = cursor.fetchone()
    assert latest_forecast[0] == timestamp
