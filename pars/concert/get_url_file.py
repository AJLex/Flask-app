import json

import requests
from bs4 import BeautifulSoup

import concert_main_functions as main_func


if __name__ == '__main__':
    #Получаем файлы с url. Аргумент это вид события: 1 - concert, 2 - theatre
    main_func.get_events_url_file(action_type_id=1) # файл - concert_urls.txt
    main_func.get_events_url_file(action_type_id=2) # файл - theatre_urls.txt


    # #Получаем информацию с сайта. Для концертов и театров получается идентичная
    # #информация.
    #
    # with open('concert_urls.txt' , 'r') as f:
    #     for line in f:
    #         url = f.readline().strip()
    #         if url:
    #             bs = BeautifulSoup(main_func.fetch_content(url),'html.parser')
    #             concert_dict = main_func.fetch_event_info(bs)
    #             # concert_dict содержит следующие ключи:
    #             # 'event title' - название,
    #             # 'event date' - дата,
    #             # 'event weekday' - день недели,
    #             # 'age limit' - возрастное ограничение,
    #             # 'place' - место проведения,
    #             # 'adress' - адресс места,
    #             # 'genre' - жанр,
    #             # 'description' - описание
    # with open('theatre_urls.txt' , 'r') as f:
    #     for line in f:
    #         url = f.readline().strip()
    #         if url:
    #             bs = BeautifulSoup(main_func.fetch_content(url),'html.parser')
    #             theatre_dict = main_func.fetch_event_info(bs)
    #             # theatre_dict содержит следующие ключи:
    #             # 'event title' - название,
    #             # 'event date' - дата,
    #             # 'event weekday' - день недели,
    #             # 'age limit' - возрастное ограничение,
    #             # 'place' - место проведения,
    #             # 'adress' - адресс места,
    #             # 'genre' - жанр,
    #             # 'description' - описание
