import requests
from app.server.server import app


def get_coordinates_by_address(address):
    """
    https://geocode-maps.yandex.ru/1.x/?format=json&geocode=Тверская+6
    :param address: address of a place e.g. Тверская+6
    :return:
    """
    response = requests.get(
        url=app.config['GEOCODE_YT_URL'], params={'format': 'json', 'geocode': '{}'.format(address)}, verify=False
    )
    print('Sending GET request to yandex geo api with geocode parameter as {}'.format(address))
    assert response.status_code == 200
    geo_code_response = response.json()
    print('Got response from yandex geo api {results}'.format(results=geo_code_response))
    assert type(geo_code_response) == dict
    try:
        geo_code_points = geo_code_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        print('Coordinates of {address} are "{points}"'.format(address=address, points=geo_code_points))
    except IndexError:
        return (None, None)
    return geo_code_points.split()


def get_mos_metro_geo_data():
    metro_name_to_coordinates_map = {}
    response = requests.get(
        url=app.config['MOS_METRO_DATA_URL'], params={'api_key': app.config['MOS_METRO_API_KEY']}, verify=False
    )
    assert response.status_code == 200
    metro_geo_data = response.json()['features']
    for metro_geo_element in metro_geo_data:
        metro_element_attributes = metro_geo_element['properties']['Attributes']
        metro_name_to_coordinates_map.update(
            {
                metro_element_attributes['NameOfStation']: (metro_element_attributes['Latitude_WGS84'],
                    metro_element_attributes['Longitude_WGS84']
                )
            }
        )
    return metro_name_to_coordinates_map




