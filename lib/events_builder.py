from datetime import datetime
from sqlalchemy import cast, Integer
from app.server.database_models import ShowEvent, Event, EventCategory, Place, MetroStations, PlaceType
from lib.dates_utils import get_this_month_date_range, get_this_year_date_range, get_this_week_date_range, \
    get_tomorrow_date_range, get_today_date_range, get_time_range_by_day_period


class Events:
    def __init__(self, event_type):
        self.event_type = event_type

    def get_filtered_events_by_category(self, db):
        return db.session.query(ShowEvent).join(Event).join(EventCategory). \
            join(Place).outerjoin(MetroStations).filter(EventCategory.category == self.event_type).all()

    def get_fresh_events(self, db):
        fresh_events = db.session.query(ShowEvent).join(Event).join(EventCategory). \
            join(Place).outerjoin(MetroStations).filter(
            (EventCategory.category == self.event_type)
        ).order_by(Event.created_at.desc()).all()
        return fresh_events

    def get_list_of_events(self, db, **kwargs):
        show_events = self.get_filtered_events_by_category(db)
        if kwargs.get('station'):
            show_events = [
                show_event for show_event in show_events if show_event.place.metro_station and
                show_event.place.metro_station.name == kwargs.get('station')
                ]
        if kwargs.get('event'):
            show_events = [
                show_event for show_event in show_events if show_event.event.name == kwargs.get('event')
                ]
        if kwargs.get('place'):
            show_events = [
                show_event for show_event in show_events if show_event.place.name == kwargs.get('place')
                ]

        if kwargs.get('dates'):
            arg_to_date_map = {
                'today': get_today_date_range(),
                'tomorrow': get_tomorrow_date_range(),
                'this_week': get_this_week_date_range(),
                'this_month': get_this_month_date_range(),
                'this_year': get_this_year_date_range()
            }

            date = arg_to_date_map[kwargs.get('dates')]

            show_events = [
                show_event for show_event in show_events if date[0] <= show_event.date_start <= date[1]
                ]
        return show_events


class ShowEvents():
    def __init__(self, event_id):
        self.event_id = event_id

    def get_filtered_show_events(self, db, **kwargs):

        event_schedule = db.session.query(ShowEvent).join(Event).join(EventCategory). \
            join(Place).outerjoin(MetroStations).filter(Event.id == self.event_id).all()

        if kwargs.get('time'):
            time_range = get_time_range_by_day_period(kwargs.get('time'))
            event_schedule = [
                showevent for showevent in event_schedule if time_range[0] <= showevent.date_start.time() <= time_range[1]
                ]
        if kwargs.get('place'):
            event_schedule = [
                showevent for showevent in event_schedule if showevent.place.name == kwargs.get('place')
                ]
        if kwargs.get('station'):
            event_schedule = [
                showevent for showevent in event_schedule if showevent.place.metro_station and
                showevent.place.metro_station.name == kwargs.get('station')
                ]
        if kwargs.get('date'):
            dates_range = kwargs.get('date').replace(" ", "").split('-')
            date_start = datetime.strptime(dates_range[0], '%m/%d/%Y').date()
            date_end = datetime.strptime(dates_range[1], '%m/%d/%Y').date()
            event_schedule = [
                showevent for showevent in event_schedule if date_start <= showevent.date_start.date() <= date_end
                ]
        return event_schedule

