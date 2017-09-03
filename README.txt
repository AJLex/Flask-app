#to apply db migration execute the following commands:

python manager.py db init
python manager.py db migrate
python manager.py db revision
python manager.py db upgrade
## apply some catalogue, like categories, age categories, place types
python manager.py seed_catalogue
## seeding test data
python manager.py seed_films
python manager.py seed_theatres
python manager.py seed_concerts
python manager.py seed_metro_stations
python manager.py seed_stations_id



#to run application:
python run.py

#to install libraries
pip install -r requirements.txt

#database models located in database_models.py

ShowEvent - для фильмов это сеанс, для концертов, выставок, спектаклей - конкретное событие в конкретном месте

Event - для фильмов это сам фильм без привязки к кинотеатру, концерт, выставка, театр - все так же, без привязки к дате и месту

Place - это кинотеатры, концертные площадки, и тд, есть имя, адресс и внешний ключ тип места на таблицу справочник PlaceTypes
есть station_id -позволяет null

MetroStations - здесь будут храниться инфа от метро с координатами

PlaceTypes - таблица справочник, тип места, кинотеатр, концертная площадка, выставочная площадка и тд, unique -name

EventCategory - таблица справочниик, фильм, спектакль, концерт и тд, unique - category

AgeCategory - таблица справочник, +0, +6 и тд, unique - category

