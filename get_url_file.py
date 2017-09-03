import json

import requests
from bs4 import BeautifulSoup

import pars.ramblerkassa.main_info_func as main_func


def get_events_file(event):
    return main_func.get_events_url_file(event)


if __name__ == '__main__':
    get_events_file('films')
    #получаем файлы с url
    # text = '1'
    # while text:
    #     text = input('Enter type of event(films, concerts, theatres) or print exit\n> ')
    #     if text != 'exit':
    #         get_events_file(text)
    #     else :
    #         break
