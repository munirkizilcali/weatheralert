from peewee import SqliteDatabase, DateTimeField, FloatField, IntegerField, BooleanField, Model
import constants

class Weather(Model):
    timestamp = DateTimeField()
    latitude = FloatField()
    longitude = FloatField()
    first_forcast = IntegerField()
    second_forcast = IntegerField()
    third_forcast = IntegerField()
    alert_generated = BooleanField(default=False)
    alert_id = IntegerField(null=True)
    
    class Meta:
        database = SqliteDatabase(constants.DATABASE_URL)
        table_name = 'weather'
