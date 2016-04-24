from utils.config import BREWERY_DB_API_KEY


def find_by_id(s, beer_id):
    query = 'https://api.brewerydb.com/v2/beer/{id}'.format(id=beer_id.encode('utf-8'))
    return _get(s, query)


def find_by_name(s, beer_name):
    url = 'https://api.brewerydb.com/v2/beers/'
    return _get(s, url, {'name': beer_name.encode('utf-8')}, meta=beer_name)


def _get(session, url, params={}, meta=None):
    params.update({'key': BREWERY_DB_API_KEY, 'format': 'json'})
    return session.get(30, url, params=params, meta=meta)
