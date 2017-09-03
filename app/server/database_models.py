from . import db


class PlaceType(db.Model):
    __tablename__ = 'place_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True) # cinema, theatre, exhibition area, concert areas
    created_at = db.Column(db.DateTime, default=db.func.now())


class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(250))
    station_id = db.Column(db.Integer, db.ForeignKey('metro_stations.id'), nullable=True)
    place_type_id = db.Column(db.Integer, db.ForeignKey('place_type.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (db.UniqueConstraint('name', 'address', name='_name_address_uc'),)

    place_type = db.relationship("PlaceType", backref='places')
    metro_station = db.relationship("MetroStations", backref='places')


class MetroStations(db.Model):
    __tablename__ = 'metro_stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    latitude = db.Column(db.Float(precision=64))
    longitude = db.Column(db.Float(precision=64))


class EventCategory(db.Model):
    __tablename__ = 'event_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), nullable=False, unique=True) #  movie,    play, exhibition,      concert
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Event type %r>' % (self.category)


class AgeCategory(db.Model):
    __tablename__ = 'age_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Age category %r>' % (self.category)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    rating = db.Column(db.String(10))
    age_category_id = db.Column(db.Integer, db.ForeignKey('age_category.id'))
    event_category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    age_category = db.relationship("AgeCategory", backref="event")
    event_category = db.relationship("EventCategory", backref="event")


class ShowEvent(db.Model):
    __tablename__ = 'show_event'
    id = db.Column(db.Integer, primary_key=True)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    price_from = db.Column(db.Integer)
    price_to = db.Column(db.Integer)
    currency = db.Column(db.String, default = 'RUB')
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    event = db.relationship("Event", backref="show_event")
    place = db.relationship("Place", backref="show_event")

