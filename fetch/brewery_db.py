import requests
from utils import brewery_db_api_key


def get_attributes():
    def attributes():
        yield 'key', brewery_db_api_key()
        yield 'format', 'json'
    return '&'.join('='.join(attr) for attr in attributes())


def find_by_id(id):
    url = 'https://api.brewerydb.com/v2/beer/{id}?'.format(id=id) + get_attributes()
    response = requests.get(url)
    return response.json()

