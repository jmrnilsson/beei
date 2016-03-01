from utils import config


def find_by_id(session, id):
    return _get(session, 'https://api.brewerydb.com/v2/beer/{id}'.format(id=id.encode('utf-8')))


def find_by_name(session, name):
    return _get(session, 'https://api.brewerydb.com/v2/beers/', {'name': name.encode('utf-8')})


def _get(session, url, params={}):
    params.update({'key': config.brewery_db_api_key(), 'format': 'json'})
    return session.get(30, url, params=params)
