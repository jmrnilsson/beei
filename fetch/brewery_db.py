from utils.config import BREWERY_DB_API_KEY


def find_by_id(s, beer_id):
    url = 'https://api.brewerydb.com/v2/beer/{id}'.format(id=beer_id.encode('utf-8'))
    result = _get(s, url)
    return result['data'] if result and result.get('data') else {}


def find_by_name(s, beer_name):
    url = 'https://api.brewerydb.com/v2/beers/'
    result = _get(s, url, {'name': beer_name.encode('utf-8')})
    return result['data'] if result and result.get('data') else {}


def apply_if_find_single_by_name(s, beer, key_name, func):
    beer_name = beer.get(key_name)
    if beer_name:
        beers = find_by_name(s, beer_name)
        if len(beers) == 1:
            func({
                'brewery_db-{1}-{0}'.format(k, key_name): v
                for k, v in beers[0].iteritems()
                if isinstance(v, basestring)
            })


def _get(session, url, params={}):
    params.update({'key': BREWERY_DB_API_KEY, 'format': 'json'})
    return session.get(30, url, params=params)
