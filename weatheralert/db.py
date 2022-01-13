import sqlite3
from typing import List, Any


class weatheralertDB:

    TABLE_NAME = "hourly_forecast"
    DATABASE_NAME = "weatheralert.db"
    LIMIT = 20

    def __init__(self) -> None:
        self.conn = None

    # allows to create a connection to db
    def connect(self) -> None:
        if self.conn is not None:
            self.close()

        self.conn = sqlite3.connect(self.DATABASE_NAME, check_same_thread=False)

    # closes connection to db
    def close(self) -> None:
        self.conn.close()
        self.conn = None

    def create_table(self):
        # create a connection to the db
        self.connect()
        c = self.conn.cursor()
        # create a table if it doesn't exist with the required columns
        c.execute(
            f""" CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    alert_generated INTEGER DEFAULT 0,
                    alert_id INTEGER DEFAULT 0,
                    first_forecast REAL,
                    longitude FLOAT,
                    latitude FLOAT,
                    second_forecast REAL,
                    third_forecast REAL,
                    timestamp REAL PRIMARY KEY
                )       
            """
        )

    # inserts a new row to the hourly_forecast table
    def insert_row(self, forecast_dict: dict) -> None:
        self.connect()
        c = self.conn.cursor()
        c.execute(
            f""" INSERT OR IGNORE INTO {self.TABLE_NAME} VALUES(
                :alert_generated, 
                :alert_id, 
                :first_forecast, 
                :latitude, 
                :longitude, 
                :second_forecast, 
                :third_forecast, 
                :timestamp
                )""",
            forecast_dict,
        )
        self.conn.commit()
        self.close()

    # query db and return all forecast entries
    def show_all(self) -> List[Any]:
        # create a connection to the db
        self.connect()
        c = self.conn.cursor()
        # execute SELECT command to get all entries from hourly_forecast table
        c.execute(
            f""" SELECT
                timestamp,
                longitude,
                latitude,
                first_forecast,
                second_forecast,
                third_forecast,
                alert_generated,
                alert_id
            FROM {self.TABLE_NAME}
            ORDER BY alert_id DESC
            LIMIT {self.LIMIT}
        """
        )
        # fetches all results
        forecasts = c.fetchall()
        # close the connection to the db
        self.conn.commit()
        self.close()

        return forecasts
