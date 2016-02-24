from utils import brewery_db_api_key, BColours, print_line


def find_by_id(session, id):
    return _get(session, 'https://api.brewerydb.com/v2/beer/{id}'.format(id=id.encode('utf-8')))


def find_by_name(session, name):
    return _get(session, 'https://api.brewerydb.com/v2/beers/', {'name': name.encode('utf-8')})


def _get(session, url, params={}):
    params.update({'key': brewery_db_api_key(), 'format': 'json'})
    return session.get(3, url, params=params)
