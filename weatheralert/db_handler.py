from typing import List
from weatheralert.db import weatheralertDB

db = weatheralertDB()
db.create_table()

# insert forecast to database
def populate_db(db: weatheralertDB, forecast_list: List[dict]) -> None:
    size = range(len(forecast_list))
    for i in size:
        db.insert_row(forecast_list[i])


# returns the db
def fetch_db():
    return db.show_all()
