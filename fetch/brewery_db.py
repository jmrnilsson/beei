from utils import config


def find_by_id(s, beer_id):
    return _get(s, 'https://api.brewerydb.com/v2/beer/{id}'.format(id=beer_id.encode('utf-8')))


def find_by_name(s, beer_name):
    return _get(s, 'https://api.brewerydb.com/v2/beers/', {'name': beer_name.encode('utf-8')})


def _get(session, url, params={}):
    params.update({'key': config.brewery_db_api_key(), 'format': 'json'})
    return session.get(30, url, params=params)
