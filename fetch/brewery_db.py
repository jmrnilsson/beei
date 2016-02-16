from http_cache import HttpCache
from utils import brewery_db_api_key


def find_by_id(id):
    return _get('https://api.brewerydb.com/v2/beer/{id}'.format(id=id))


def find_by_name(name):
    return _get('https://api.brewerydb.com/v2/beers/', {'name': name})


def _get(url, params={}):
    params.update({'key': brewery_db_api_key(), 'format': 'json'})
    return HttpCache(3).get(url, params)
