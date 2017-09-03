import json
from flask import Flask, render_template, request
from . import db
from . import create_app
from app.server.database_models import ShowEvent, Event, EventCategory, Place, MetroStations, PlaceType
from lib.events_builder import Events, ShowEvents

app = create_app(config_name='default')


def get_places_json_by_place_type(place_type):
    places_list = db.session.query(Place).join(PlaceType).filter(PlaceType.type == place_type).all()
    return json.dumps([place.name for place in places_list])


def get_metro_source_json_data():
    metro_stations_list = db.session.query(MetroStations).all()
    return json.dumps([metro.name for metro in metro_stations_list])


@app.route('/')
def index_page():
    concert_events = Events(event_type='Концерт').get_fresh_events(db)[:3]
    movie_events = Events(event_type='Фильм').get_fresh_events(db)[:3]
    play_events = Events(event_type='Спектакль').get_fresh_events(db)[:3]
    return render_template("index.html", concert_events=concert_events, movie_events=movie_events, play_events=play_events)


@app.route('/concerts/')
def concerts():
    dates = request.args.get('dates')
    station = request.args.get('station')
    place = request.args.get('place')
    event_name = request.args.get('event')
    kwargs = {'dates': dates, 'station': station, 'place': place, 'event': event_name}
    show_concert_events = Events(event_type='Концерт').get_list_of_events(db, **kwargs)
    distinct_event_list = []

    for show_event in show_concert_events:
        event_names = [event.event.name for event in distinct_event_list]
        if show_event.event.name not in event_names:
            distinct_event_list.append(show_event)
    distinct_event_list_names = list(set([concert.event.name for concert in show_concert_events]))
    return render_template(
        "concerts.html", events=distinct_event_list, metro_data_source_json=get_metro_source_json_data(),
        place_data_source_json=get_places_json_by_place_type(place_type='Концертные площадки'),
        event_list_to_json=json.dumps(distinct_event_list_names)
    )


@app.route('/concert/<path:eventId>')
def concert(eventId):
    date = request.args.get('date')
    time = request.args.get('time')
    station = request.args.get('station')
    place = request.args.get('place')
    kwargs = {'date': date, 'time': time, 'station': station, 'place': place}
    event_info = db.session.query(Event).filter(Event.id == eventId).one()
    concert_schedule = ShowEvents(event_id=eventId).get_filtered_show_events(db, **kwargs)
    return render_template(
        "concert.html", event_info=event_info, event_schedule=concert_schedule, metro_data_source_json=get_metro_source_json_data(),
        place_data_source_json=get_places_json_by_place_type(place_type='Концертные площадки')
    )


@app.route('/movies/')
def movies():
    dates = request.args.get('dates')
    station = request.args.get('station')
    place = request.args.get('place')
    movie_name = request.args.get('event')
    kwargs = {'dates': dates, 'station': station, 'place': place, 'event': movie_name}
    show_movie_events = Events(event_type='Фильм').get_list_of_events(db, **kwargs)

    distinct_event_list = []

    for show_event in show_movie_events:
        event_names = [event.event.name for event in distinct_event_list]
        if show_event.event.name not in event_names:
            distinct_event_list.append(show_event)

    distinct_event_list_names = list(set([movie.event.name for movie in show_movie_events]))
    return render_template(
        "movies.html", events=distinct_event_list, metro_data_source_json=get_metro_source_json_data(),
        place_data_source_json=get_places_json_by_place_type(place_type='Кинотеатры'),
        event_list_to_json=json.dumps(distinct_event_list_names)
    )


@app.route('/movie/<path:eventId>')
def movie(eventId):
    date = request.args.get('date')
    time = request.args.get('time')
    station = request.args.get('station')
    place = request.args.get('place')
    kwargs = {'date': date, 'time': time, 'station': station, 'place': place}
    event_info = db.session.query(Event).filter(Event.id == eventId).one()
    movie_schedule = ShowEvents(event_id=eventId).get_filtered_show_events(db, **kwargs)
    return render_template(
        "movie.html", event_info=event_info, event_schedule=movie_schedule, metro_data_source_json=get_metro_source_json_data(),
        place_data_source_json=get_places_json_by_place_type(place_type='Кинотеатры')
    )


@app.route('/theatres/')
def theatres():
    dates = request.args.get('dates')
    station = request.args.get('station')
    place = request.args.get('place')
    play_name = request.args.get('event')
    kwargs = {'dates': dates, 'station': station, 'place': place, 'event': play_name}
    show_play_events = Events(event_type='Спектакль').get_list_of_events(db, **kwargs)
    distinct_event_list = []

    for show_event in show_play_events:
        event_names = [event.event.name for event in distinct_event_list]
        if show_event.event.name not in event_names:
            distinct_event_list.append(show_event)
    distinct_event_list_names = list(set([movie.event.name for movie in show_play_events]))
    return render_template(
        "theatres.html", events=distinct_event_list, metro_data_source_json=get_metro_source_json_data(),
        place_data_source_json=get_places_json_by_place_type(place_type='Театры'),
        event_list_to_json=json.dumps(distinct_event_list_names)
    )


@app.route('/theatre/<path:eventId>')
def theatre(eventId):
    date = request.args.get('date')
    time = request.args.get('time')
    station = request.args.get('station')
    place = request.args.get('place')
    kwargs = {'date': date, 'time': time, 'station': station, 'place': place}
    event_info = db.session.query(Event).filter(Event.id == eventId).one()
    theatre_schedule = ShowEvents(event_id=eventId).get_filtered_show_events(db, **kwargs)
    return render_template(
        "theatre.html", event_info=event_info, event_schedule=theatre_schedule, metro_data_source_json=get_metro_source_json_data(),
        place_data_source_json=get_places_json_by_place_type(place_type='Театры')
    )