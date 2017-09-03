import requests
from bs4 import BeautifulSoup


def get_month(month):
    ru_month_values = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 10,
        'декабря': 12,
    }
    return ru_month_values.get(month)


def fetch_content(url, params=None):
    try:
        result = requests.get(url, params=params)
        result.raise_for_status()
        return result.text
    except (requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError) as e:
        print(e)


def fetch_number_of_events_and_urls(action_type_id=None, page=1):
    url = 'http://concert.ru/Home/Events'
    params = {
                'Page': page,
                'ActionTypeID': action_type_id
             }
    events_url = []
    raw_number = []
    html = fetch_content(url, params)
    bs = BeautifulSoup(html, 'html.parser')
    raw_data = bs.find('div', class_='pagination')
    for raw in raw_data.find_all('span'):
        raw_number.append(raw.text)
    for raw_data in bs.find_all('div', class_="event event_horizontal"):
        events_url.append('http://concert.ru' + \
                          raw_data.find('a', class_="event__name").get('href'))
    current_page = page
    return int(raw_number[0].split('-')[-1]), events_url, raw_number[1], current_page


def get_events_url_file(action_type_id):
    current_events, events_url_list, number_of_events,\
    current_page = fetch_number_of_events_and_urls(action_type_id)
    events_url_lists = []
    next_events = int(current_events)
    while int(current_events) < int(number_of_events):
        current_page += 1
        events_url_lists += events_url_list
        current_events += next_events
        events_url_list = fetch_number_of_events_and_urls(action_type_id,
                                                        current_page)[1]
        print(current_events, number_of_events)
    if action_type_id == 1:
        file_name = 'concert_urls.txt'
    else:
        file_name = 'theatre_urls.txt'
    with open(file_name, 'w') as f:
        for url in events_url_lists:
            f.write(url + '\n')



def fetch_event_header(bs):
    raw_data = bs.find('div', class_="eventHeader")
    if raw_data:
        return (raw_data.find('h2', class_="eventHeader__title"),
                raw_data.find('div', class_="eventHeader__age"),
                raw_data.find('div', class_="eventHeader__hall"),
                raw_data.find('div', class_="eventHeader__address"))


def fetch_event_date(bs):
    raw_data = bs.find('div', class_="eventTabs")
    if raw_data:
        return raw_data.find('span', class_="eventTabs__tableDate"),\
               raw_data.find('div', class_="eventTabs__tableTime")


def fetch_event_genre_and_description(bs):
    raw_data = bs.find('div', class_="eventInfo")
    if raw_data:
        return (raw_data.find('h2', class_="eventInfo__title"),
               raw_data.find('div', class_="eventInfo__body"))


def fetch_event_info(bs):
    header_html = fetch_event_header(bs)
    other_info_html =  fetch_event_genre_and_description(bs)
    raw_date = fetch_event_date(bs)[0].text.strip().split('\r') if fetch_event_date(bs)[0] else None
    raw_time = fetch_event_date(bs)[1].text if fetch_event_date(bs)[1] else None
    print(header_html[0].text.strip())
    return {
        'event title': header_html[0].text.strip(),
        'event time': raw_time,
        'event date': raw_date[0] if raw_date else None,
        'event weekday': raw_date[1].strip().strip('(').strip(')') if raw_date else None,
        'age limit': header_html[1].text.strip() if header_html[1] else None,
        'place': header_html[2].text if header_html[2] else None,
        'adress': header_html[3].text if header_html[3] else None,
        'genre':other_info_html[0].text if other_info_html[0] else None,
        'description': other_info_html[1].text.strip() if other_info_html[1] else None
    }


def fetch_all_events_info(urls_file):
    events_info_list = []
    with open(urls_file, 'r') as f:
        for line in f:
            url = f.readline().strip()
            bs = BeautifulSoup(fetch_content(url), 'html.parser')
            events_info_list.append(fetch_event_info(bs))
    return events_info_list
