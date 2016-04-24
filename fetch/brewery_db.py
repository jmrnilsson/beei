from utils.config import BREWERY_DB_API_KEY


def find_by_id(s, beer_id):
    url = 'https://api.brewerydb.com/v2/beer/{id}'.format(id=beer_id.encode('utf-8'))
    result = _get(s, url)
    return result['data'] if result and result.get('data') else {}


def find_by_name(s, beer_name):
    url = 'https://api.brewerydb.com/v2/beers/'
    result = _get(s, url, {'name': beer_name.encode('utf-8')})
    return result['data'] if result and result.get('data') else {}


def _get(session, url, params={}):
    params.update({'key': BREWERY_DB_API_KEY, 'format': 'json'})
    return session.get(30, url, params=params)
