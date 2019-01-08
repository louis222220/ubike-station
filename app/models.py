from app.__init__ import db


class FavoriteStation(db.Model):
    __tablename__ = 'favorite_stations'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))
    created_time = db.Column(db.TIMESTAMP(True), nullable=False)


class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    station_no = db.Column(db.Integer, nullable=True)
    favorites = db.relationship(
        'FavoriteStation', backref='stations', lazy='dynamic')
