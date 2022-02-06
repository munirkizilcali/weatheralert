from peewee import (
    BooleanField,
    DateTimeField,
    FloatField,
    IntegerField,
    Model,
    SqliteDatabase,
)

import constants


class Weather(Model):
    timestamp = DateTimeField()
    latitude = FloatField()
    longitude = FloatField()
    first_forecast = IntegerField()
    second_forecast = IntegerField()
    third_forecast = IntegerField()
    alert_generated = BooleanField(default=False)
    alert_id = IntegerField(null=True)

    class Meta:
        database = SqliteDatabase(constants.DATABASE_URL, check_same_thread=False)
        table_name = "weather"
