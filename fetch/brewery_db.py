import requests
from utils import brewery_db_api_key


def find_by_id(id):
    return __get('https://api.brewerydb.com/v2/beer/{id}'.format(id=id))


def find_by_name(name):
    return __get('https://api.brewerydb.com/v2/beers/', {'name': name})


def __get(url, params={}):
    params.update({'key': brewery_db_api_key(), 'format': 'json'})
    return requests.get(url, params).json()
