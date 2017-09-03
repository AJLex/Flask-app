import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join('sqlite:///', basedir, 'app.db'))
    GEOCODE_YA_URL = 'https://geocode-maps.yandex.ru/1.x/'
    MOS_METRO_DATA = {
        'url': "https://apidata.mos.ru/v1/datasets/624/features",
        'api_key': '44ba1a25a85f563cee0569a253c6e77c'}

    @staticmethod
    def init_app(app):
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
        app.config['GEOCODE_YT_URL'] = Config.GEOCODE_YA_URL
        app.config['MOS_METRO_DATA_URL'] = Config.MOS_METRO_DATA['url']
        app.config['MOS_METRO_API_KEY'] = Config.MOS_METRO_DATA['api_key']



config = {
    'default': Config
}