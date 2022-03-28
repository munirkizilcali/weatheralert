from app import db


class ForecastModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    long = db.Column(db.Float)
    lat = db.Column(db.Float)
    first_forecast = db.Column(db.Integer)
    second_forecast = db.Column(db.Integer)
    third_forecast = db.Column(db.Integer)
    alert_generated = db.Column(db.Boolean)
    alert_id = db.Column(db.Integer)

    def __repr__(self):
        return 'timestamp <{}>'.format(self.timestamp)

